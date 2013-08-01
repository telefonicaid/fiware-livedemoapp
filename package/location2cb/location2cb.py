#!/usr/bin/python
# Copyright 2013 Telefonica Investigación y Desarrollo, S.A.U
#
# This file is part of FI-WARE LiveDemo App
#
# This file is part of FI-WARE LiveDemo App is free software: you can redistribute it and/or modify it under the terms
# of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# FI-WARE LiveDemo App is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License
# for more details.
#
# You should have received a copy of the GNU Affero General Public License along with FI-WARE LiveDemo App. If not,
# see http://www.gnu.org/licenses/.
#
# For those usages not covered by the GNU Affero General Public License please contact with fermin at tid dot es

__author__ = 'fermin'

from sys import argv
from time import sleep
from requests import post
from locs_sim import get_location, load_points, allPoints, define_route

def update_van_locations_xml(locations):

    s = ''
    s += '<?xml version="1.0" encoding="UTF-8"?>\n'
    s += '<updateContextRequest>\n'
    s += '  <contextElementList>\n'

    for van in locations.keys():
        s += '    <contextElement>\n'
        s += '      <entityId type="Van" isPattern="false">\n'
        s += '	      <id>' + van + '</id>\n'
        s += '	    </entityId>\n'
        s += '      <contextAttributeList>\n'
        s += '        <contextAttribute>\n'
        s += '          <name>current_position</name>\n'
        s += '          <contextValue>' + locations[van] + '</contextValue>\n'
        s += '        </contextAttribute>\n'
        s += '      </contextAttributeList>\n'
        s += '    </contextElement>\n'

    s += '  </contextElementList>\n'
    s += '  <updateAction>UPDATE</updateAction>\n'
    s += '</updateContextRequest>\n'
    return s

def do_post(url, data):

    # Setting the content-type is important: otherwise ContextBroker will don't process the request
    headers = {}
    headers['Content-Type'] = 'application/xml'
    return post(url, data, headers=headers)

# FIXME: unhardwire variables
cb_url = 'http://localhost:1026/'

technitians = [ '34669079467',
                '34604872235',
                '32026548889',
                '32026171005'
                ]

vans = {technitians[0]: 'van1',
        technitians[1]: 'van2',
        technitians[2]: 'van3',
        technitians[3]: 'van4'
        }

# Used without arguments, this script is just a location-CB updater for
# all the tecniians. Used with arguments, it moves a single technitian
# (working in the same way than move_van.py script)
autonomous = False
route_pointer = 0
if len(argv) > 1:
    tech = argv[1]
    origin = argv[2]
    destination = argv[3]
    print 'working on autonomous mode'
    autonomous = True

    load_points('points.csv')
    #print str(allPoints)

    route = define_route(origin, destination)
    #print str(route)
    max = len(route)

    # Reduce the technitians list to only the one in the arguments
    technitians = [ tech ]

    wait = 3

else:
    wait = 1
    # "Fake" values that we need to make while loop infinite
    max = 10

# Note that in the case of no autonomous mode, max is never reached no matter its value, as
# route_pointer is never increased
while route_pointer < max:
    locations = {}
    for t in technitians:

        if autonomous:
            # Get location from points
            loc_str =  allPoints[route[route_pointer]][0] + ', ' + allPoints[route[route_pointer]][1]
            route_pointer += 1
        else:
            # Get location from Location GE
            loc = get_location(t)
            loc_str = str(loc[0]) + ', ' + str(loc[1])

        locations[vans[t]] = loc_str

    # Update Context Broker information
    print 'update with: ' + str(locations)
    do_post(cb_url + 'NGSI10/updateContext', update_van_locations_xml(locations))

    # Sleep for a while before doing the process again
    sleep(wait)

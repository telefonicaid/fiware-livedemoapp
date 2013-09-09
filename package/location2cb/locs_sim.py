# -*- coding: latin-1 -*-
# Copyright 2013 Telefonica Investigación y Desarrollo, S.A.U
#
# This file is part of FI-WARE LiveDemo App
#
# FI-WARE LiveDemo App is free software: you can redistribute it and/or modify it under the terms
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

__author__ = 'sergg'

import requests
import time
from xml.dom.minidom import parse, parseString
from env import locs_host

simulation_tool_url = 'http://' + locs_host + ':8111/testtool/simulation/mobilepaths'
simulation_mobile_url = 'http://' + locs_host +':8111/testtool/simulation/mobilepath/'
google_maps_url = "https://maps.google.com/maps?q="

scenario_control_url = 'http://' + locs_host + ':8111/testtool/scenario/control?'
location_query_url =  'http://' + locs_host + ':3128/location/v1/queries/location?requester=locationGE:fiware&requestedAccuracy=50&acceptableAccuracy=60&maximumAge=100&tolerance=DelayTolerant&address='

allPoints = dict()

technician_A = "34669079467"
technician_B = "34604872235"
technician_C = "32026548889"
technician_D = "32026171005"

def init():
    load_points("points.csv")
    load_simulation(generate_route(technician_A , ["A1","A2"],False,True))
    load_simulation(generate_route(technician_B , ["B1","B2"],False,True))
    load_simulation(generate_route(technician_C ,["C1","C2","C3","C3","C5","C6","C7","C8","C9","C10","C1" ],True,True))
    load_simulation(generate_route(technician_D ,["D1","D2","D3","D3","D5","D1" ],True,True))

    init_simulation("LocationGE-LocationQuery")
    start_simulation()

    start(technician_C)
    start(technician_D)
    get_path(technician_A)

    start(technician_A)
    stop(technician_A)
    start(technician_B)
    stop(technician_B)

    time.sleep(2)



def stop_scenario():
    stop(technician_A)
    stop(technician_B)
    stop(technician_C)
    stop(technician_D)

    stop_simulation()


def define_route( from_point, to_point):

    forth_route_A = ["A1", "A2", "A3", "A4", "A5"]
    back_route_A =  ["A5", "A4", "A3", "A2", "A1"]
    forth_route_B = ["B1", "B2", "B3", "B4"]
    back_route_B = ["B4", "B3", "B2", "B1"]

    if from_point == "A1":
        forth_route_A.append(to_point)
        print "new route " + str(forth_route_A)
        return forth_route_A
    elif from_point == "B1":
        forth_route_B.append(to_point)
        print "new route " +  str(forth_route_B)
        return  forth_route_B
    elif to_point == "A1":
            back_route_A.insert(0,from_point)
            print "new route " +  str(back_route_A)
            return back_route_A
    elif to_point == "B1":
            back_route_B.insert(0,from_point)
            print "new route " +  str(back_route_B)
            return back_route_B
    else:
        return None


def move_van(technician,from_, to_, loop,auto):
    stop(technician)
    #delete_simulation(technician)
    load_simulation(generate_route(technician,define_route(from_,to_) ,loop,auto))
    start(technician)

def get_position(technician):
    return get_location(technician)


def load_points(filename):
    csv = open(filename,'r')
    for line in csv:
        if not line: break
        point = line.split(';')
        allPoints[point[0]]=(point[1],point[2])
        #print point
    csv.close()

def get_point(point):
    return allPoints[point]


def generate_route(msisdn,route,autoloop,automove):

    load_points("points.csv")

    template = parseString((open("template.xml", 'r')).read())
    template.getElementsByTagName('msisdn')[0].appendChild(template.createTextNode(msisdn))
    template.getElementsByTagName('name')[0].appendChild(template.createTextNode(msisdn + " from " + route[0] + " to " + route[-1]))
    template.getElementsByTagName('autoLoop')[0].appendChild(template.createTextNode(str(autoloop).lower()))
    template.getElementsByTagName('autoMove')[0].appendChild(template.createTextNode(str(automove).lower()))

    for point in route:
        #print point
        pointChild =  parseString( "\t<position> \n \
            <name></name> \n \
            <latitude></latitude> \n \
            <longitude></longitude> \n \
            <altitude></altitude> \n \
          </position> \n")
        if allPoints.has_key(point):
            point_name = pointChild.createTextNode(point)
            pointChild.getElementsByTagName('name')[0].appendChild(point_name)
            point_lat = pointChild.createTextNode(allPoints[point][0])
            pointChild.getElementsByTagName('latitude')[0].appendChild(point_lat)
            point_long = pointChild.createTextNode(allPoints[point][1])
            pointChild.getElementsByTagName('longitude')[0].appendChild(point_long)
            point_alt = pointChild.createTextNode("12.0")
            pointChild.getElementsByTagName('altitude')[0].appendChild(point_alt)
            #print pointChild.toxml()
            template.getElementsByTagName('positions')[0].appendChild(template.importNode(pointChild.childNodes[0],True))
        else:
            print "Missing point " + point

        #template.getElementsByTagName('positions')[0].appendChild(template.createElement("position"))

    #print template.toxml()
    writeToFile=False
    if writeToFile:
        route = open(msisdn +".xml",'w')
        route.write(template.toxml())
        route.close()

    return template.toxml()

def init_simulation(scenario):
    print "#init simulation of " + scenario + " scenario..."
    url = scenario_control_url+"select=" + scenario
    #print "PUT " + url
    control_request = requests.put(url)
    #print str(control_request.status_code)
    #print control_request.text


def start_simulation():
    url = scenario_control_url+"cmd=start"
    print "start simulation PUT " + url
    start_request = requests.put(scenario_control_url+"cmd=start")
    #print str(start_request.status_code)
    #print start_request.text

def load_simulation_from_file(technician):
    #print "#loading " + technician + " simulation..."
    fragment_file = open(technician + '.xml','r')
    simulation_fragment = fragment_file.read()
    #print "POST " + simulation_tool_url
    headers = {'content-type': 'application/xml'}
    r = requests.post(simulation_tool_url, data = simulation_fragment , headers = headers)
    #print r.status_code
    #print r.text
    fragment_file.close()

def load_simulation(simulation_fragment):
    print "#loading  simulation..."
    #print "POST " + simulation_tool_url
    headers = {'content-type': 'application/xml'}
    r = requests.post(simulation_tool_url, data = simulation_fragment , headers = headers)
    #print r.status_code
    #print r.text


def delete_simulation(technician):
    print "#delete " + technician + " path..."
    request_url = simulation_mobile_url + technician
    #print "DELETE  " + request_url
    headers = {'content-type': 'application/xml'}
    start_request = requests.delete(request_url, headers = headers)
    #print str(start_request.status_code) + " " + start_request.text


def start(technician):
    print "#start " + technician + " simulation..."
    request_url = simulation_mobile_url + technician+"?stationary=false"
    #print "PUT " + request_url
    start_request = requests.put(request_url)
    #print str(start_request.status_code)
    #print start_request.text


def get_path(technician):
    print "#get_path " + technician + " simulation..."
    request_url = simulation_mobile_url + technician
    #print "GET " + request_url
    headers = {'content-type': 'application/xml'}
    start_request = requests.get(request_url, headers = headers)
    print str(start_request.status_code) + " " + start_request.text

def stop(technician):
    print "#stop " + technician + " simulation..."
    request_url = simulation_mobile_url + technician+"?stationary=true"
    #print "PUT " + request_url
    start_request = requests.put(request_url)
    #print str(start_request.status_code)
    #print start_request.text


def stop_simulation():
    print "Stop simulation PUT " + scenario_control_url+"cmd=stop"
    control_request = requests.put(scenario_control_url+"cmd=stop")
    #print str(control_request.status_code) + " " + control_request.text

def pause_simulation():
    print "pause  simulation..."
    control_request = requests.put(scenario_control_url+"cmd=pause")
    #print str(control_request.status_code) + " " + control_request.text



def get_location(technician):
    #print "#get " + technician + " location ..."
    headers = {'content-type': 'application/json'}
    #print "GET "+  location_query_url + technician
    r = requests.put(location_query_url + technician , headers = headers)
    #print "-->DEBUG"
    #print str(r.status_code)
    #print r.json()
    #print "<--DEBUG"
    location = r.json()

    if location.has_key("terminalLocation"):
        longitude = location["terminalLocation"][0]["currentLocation"]["latitude"]
        latitude = location["terminalLocation"][0]["currentLocation"]["longitude"]
        timestamp = location["terminalLocation"][0]["currentLocation"]["timestamp"]
        show_location(longitude,latitude)
        return (longitude,latitude)
    else:
        print location


def show_googlemap(longitude,latitude):
    print time.ctime() + ": " + google_maps_url+ str(longitude)  + "," + str(latitude)

def show_location(longitude,latitude):
    print str(longitude)  + "," + str(latitude)


def main():

    init()
    for i in range(2):
        get_position(technician_A)
        get_position(technician_B)
        get_position(technician_C)
        get_position(technician_D)
        time.sleep(10)

    move_van(technician_A,"A1","E7",False,True)
    get_path(technician_A)

    move_van(technician_B,"B1","E2",False,True)
    get_path(technician_B)

    for i in range(2):
        get_position(technician_A)
        get_position(technician_B)
        get_position(technician_C)
        get_position(technician_D)
        time.sleep(10)

    stop_scenario()




if __name__ == '__main__':
    main()

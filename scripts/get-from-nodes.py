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

import subprocess
from lxml import etree
from sys import argv, exit

allowed_attrs = ['TimeInstant', 'Latitud', 'Longitud', 'presence', 'batteryCharge', 'illuminance']

# Arguments from command line
if len(argv) < 2:
    print 'wrong number of arguments'
    exit(1)

attr = argv[1]
if not attr in allowed_attrs:
    print attr + ' is not an allowed attribute for Node'
    print 'allowed ones: ' + str(allowed_attrs)
    exit(1)

p = subprocess.Popen(['./query-node.sh'], shell=False, stdout=subprocess.PIPE)
output = p.stdout.read()

doc = etree.fromstring(output)

for ce in doc.findall('.//contextElement'):
    id = ce.find('.//id').text
    value = None
    for ca in ce.findall('.//contextAttribute'):
        if (ca.find('name').text == attr):
            value = ca.find('contextValue').text

    print repr(id).ljust(35), ": ", value


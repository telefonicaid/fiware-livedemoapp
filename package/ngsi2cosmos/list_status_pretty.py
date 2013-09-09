#!/usr/bin/python
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

__author__ = 'fermin'

import subprocess
import json
from datetime import datetime
from ngsi2cosmos import cosmos_url

url = cosmos_url + '/webhdfs/v1/user/livedemo?op=liststatus&user.name=livedemo'
p = subprocess.Popen(['curl', '-s', url], shell=False, stdout=subprocess.PIPE)
doc = json.loads(p.stdout.read())

file_info = {}
for file in doc['FileStatuses']['FileStatus']:
    info = []
    human_date = str(datetime.fromtimestamp(file['modificationTime']/1000))
    info.append(str(file['pathSuffix']))
    info.append(str(file['length']))
    info.append(human_date)
    # We are using as key the concatenation of modificationTime and pathSuffix, to ensure uniqueness
    id = str(file['modificationTime']) + ':' + file['pathSuffix']
    file_info[id] = info

n = 0
keys = file_info.keys()
keys.sort()
keys.reverse()
for id in keys:
    print repr(file_info[id][0]).ljust(115), ': ', repr(file_info[id][2]).ljust(20), ': ', file_info[id][1]
    n += 1

print 'Total files: ' + str(n)


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

p = subprocess.Popen(["./query-all.sh"], shell=False, stdout=subprocess.PIPE)
output = p.stdout.read()

doc = etree.fromstring(output)

for ce in doc.findall('.//contextElement'):
    id = ce.find('.//id').text
    time_instant = None
    for ca in ce.findall('.//contextAttribute'):
        if (ca.find('name').text == 'TimeInstant'):
            time_instant = ca.find('contextValue').text

    print repr(id).ljust(35), ": ", str(time_instant)


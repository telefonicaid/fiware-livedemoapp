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

import locs_sim as locs
import sys
import time

def print_positions():
        print 'Technician A (' + locs.technician_A + '):',
        locs.get_location(locs.technician_A)
        print 'Technician B (' + locs.technician_B + '):',
        locs.get_location(locs.technician_B)
        print 'Technician C (' + locs.technician_C + '):',
        locs.get_location(locs.technician_C)
        print 'Technician D (' + locs.technician_D + '):',
        locs.get_location(locs.technician_D)

def main():

    sleep = 5.0
    times = 1

    print "Usage: python get_vans.py [period (default = 5 seconds)] [times (default once) (0 = forever)]"

    if len(sys.argv) > 1:
        sleep = float(sys.argv[1])
    if len(sys.argv) > 2:
        times = int(sys.argv[2])

    if times == 0:
        while True:
            print_positions()
            time.sleep(sleep)
    else:
        for i in range(0,times):
            print_positions()
            time.sleep(sleep)


if __name__ == '__main__':
    main()

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

__author__ = 'sergg'

import locs_sim as locs
import sys

def main():


    if len(sys.argv) != 4:
        print "Usage: python move_van.py [van_msisdn] [from] [to]"
        print "ej: python move_van.py 34621898316 A1 E7"
        return

    van = sys.argv[1]
    from_point = sys.argv[2]
    to_point = sys.argv[3]

    print "Moving " + van + " from " + str(from_point) +  " to " + str(to_point)
    locs.move_van(van,from_point,to_point,False,True)
    locs.get_path(van)

if __name__ == '__main__':
    main()

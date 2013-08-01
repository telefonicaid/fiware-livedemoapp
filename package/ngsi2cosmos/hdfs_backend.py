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

from abc import ABCMeta, abstractmethod

'''
Abstract parent class for all HDFS backend
'''
class HdfsBackend:

    __metaclass__ = ABCMeta

    def __init__(self, logger, cosmos_url, base_dir, cosmos_user):
        self.logger = logger
        self.cosmos_url = cosmos_url
        self.base_dir = base_dir
        self.cosmos_user = cosmos_user

    '''
    cosmos_append

    Append line to file in HDFS backend, abstracting all the low level details
    '''
    @abstractmethod
    def cosmos_append(self, file_name, line):
        pass


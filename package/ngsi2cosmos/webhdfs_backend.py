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

from hdfs_backend import HdfsBackend
from requests_wrappers import do_post, do_get, do_put
import re

'''
WebHDFS implementation of the HDFS persistence backend
'''
class WebHdfsBackend(HdfsBackend):

    def __init__(self, logger, cosmos_url, base_dir, cosmos_user, dn_map):
        self.dn_map = dn_map
        HdfsBackend.__init__(self, logger, cosmos_url, base_dir, cosmos_user)


    '''
    cosmos_append

    Append line to file in HDFS backend, abstracting all the low level details
    '''
    def cosmos_append(self, file_name, line):

        # First, check that the file exists, creating it otherwise
        if not self._cosmos_file_exists(file_name):
            self._cosmos_create(file_name)

        # Step 1: interact with the namenode
        url = self.cosmos_url + '/webhdfs/v1' + self.base_dir + '/' + file_name + '?op=append&user.name=' + self.cosmos_user
        r = do_post(self.logger, url)
        if r.status_code != 307:
            raise Exception('expecting 307 but getting ' + str(r.status_code))

        # Grab datanode from Location header
        actual_datanode = self._resolve_datanode(r.headers['Location'])

        # Step 2: interact with the datanode
        url = 'http://' + actual_datanode + '/webhdfs/v1' + self.base_dir + '/' + file_name + '?op=append&user.name=' + self.cosmos_user
        r = do_post(self.logger, url, line)
        if r.status_code != 200:
            raise Exception('expecting 200 but getting ' + str(r.status_code))


    '''
    _cosmos_create

    Create a file in the HDFS backend
    '''
    def _cosmos_create(self, file_name):
        # Step 1: interact with the namenode
        url = self.cosmos_url + '/webhdfs/v1' + self.base_dir + '/' + file_name + '?op=create&user.name=' + self.cosmos_user
        r = do_put(self.logger, url)
        if r.status_code != 307:
            raise Exception('expecting 307 but getting ' + str(r.status_code))

        # Grab datanode from Location header
        actual_datanode = self._resolve_datanode(r.headers['Location'])

        # Step 2: interact with the datanode
        url = 'http://' + actual_datanode + '/webhdfs/v1' + self.base_dir + '/' + file_name + '?op=create&user.name=' + self.cosmos_user
        r = do_put(self.logger, url)
        if r.status_code != 201:
            raise Exception('expecting 201 but getting ' + str(r.status_code))

    '''
    cosmos_create_base_dir

    Create a directory tree in the HDFS backend corresponding to the base directory given as argument
    '''
    def cosmos_create_base_dir(self):
        # Single step operation (no interaction with the datanodes)
        url = self.cosmos_url + '/webhdfs/v1' + self.base_dir + '?op=mkdirs&user.name=' + self.cosmos_user
        r = do_put(self.logger, url)
        if r.status_code != 200:
            raise Exception('expecting 200 but getting ' + str(r.status_code))

    '''
    _cosmos_file_exists

    Checks wether a file exists in the HDFS backend (returning true or false)
    '''
    def _cosmos_file_exists(self, file_name):
        url = self.cosmos_url + '/webhdfs/v1' + self.base_dir + '/' + file_name + '?op=getfilestatus&user.name=' + self.cosmos_user
        r = do_get(self.logger, url)

        if r.status_code == 500:
            raise Exception('server internal error while retrieving file status')

        if r.status_code == 200:
            return True
        else:
            return False

    '''
    _resolve_datanode

    Uses the internal dictionary to translate between datanodes (as found in
    Location header in HTTP move responses) to the actual datanode
    '''
    def _resolve_datanode(self, loc):

        m = re.match('http://(.*)/webhdfs', loc)
        dn = m.group(1)
        self.logger.debug('  datanode is: ' + dn)

        if not self.dn_map.has_key(dn):
            raise Exception('cannot resolve datanode ' + dn)
        else:
            actual_datanode = self.dn_map[dn]
            self.logger.debug('  actual datanode is: ' + actual_datanode)
            return actual_datanode

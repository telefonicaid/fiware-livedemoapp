#!/usr/bin/python
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

from requests import get, put, post

'''
do_get

Wrapper method for requests get
'''
def do_get(logger, url, headers=None):
    logger.info('   --> GET ' + url)
    r = get(url, headers=headers)
    logger.info('   <-- ' + str(r.status_code))
    if len(r.text) != 0:
        logger.debug('  <-- ' + r.text)
    return r

'''
do_post

Wrapper method for requests post
'''
def do_post(logger, url, data=None, headers=None):
    logger.info('   --> POST ' + url)
    # We disable redirection, given that we need to manage it in our code; this is due to we cannot rely
    # on proper name resolution of the hostnames in the Location header
    r = post(url, data, headers=headers, allow_redirects=False)
    logger.info('   <-- ' + str(r.status_code))
    if len(r.text) != 0:
        logger.debug('  <-- ' + r.text)
    return r

'''
do_put

Wrapper method for requests put
'''
def do_put(logger, url, data=None, headers=None):
    logger.info('   --> PUT ' + url)
    # We disable redirection, given that we need to manage it in our code; this is due to we cannot rely
    # on proper name resolution of the hostnames in the Location header
    r = put(url, data, headers=headers, allow_redirects=False)
    logger.info('   <-- ' + str(r.status_code))
    if len(r.text) != 0:
        logger.debug('  <-- ' + r.text)
    return r
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

from flask import Flask, request, Response
from lxml import etree
from requests import Timeout, ConnectionError
import logging
from datetime import datetime
from sys import argv
from httpfs_backend import HttpFsBackend
from webhdfs_backend import WebHdfsBackend
import re
from env import cosmos_url, cosmos_user, base_dir
from hive import HiveClient

# Constants
delimiter = '|'

# FIXME: this should be unhardwired, moved to a configuration file
dn_map = {
    'cosmosslave1-gi:50075': 'localhost:52875',
    'cosmosslave2-gi:50075': 'localhost:52975',
    }

# FIXME: backend selection should me moved to a configuration file
hdfs_backend = 'HttpFS'

# Default arguments
port = 1028
default_timeout = 3
actual_base_dir = base_dir
log_off = False

# FIXME: this way of processing arguments doesn't scale very well, we need
# a better approach
# Arguments from command line
if len(argv) > 2:
    port = int(argv[1])
    cosmos_url = argv[2]
if len(argv) > 3:
    actual_base_dir = argv[3]
if len(argv) > 4:
    cosmos_user = argv[4]
if len(argv) > 5:
    if argv[5] == "log_off":
        log_off = True

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def process_notify():

    app.logger.info('====================================================')

    if (len(request.data) == 0):
        app.logger.info('Empty notification message')
        return Response(status=200)

    app.logger.debug('New notification (raw): \n' + request.data)

    doc = etree.fromstring(request.data)

    # Process the elements ContextElementResponse list
    for cer in doc.findall('.//contextElementResponse'):
        process_cer(cer)

    return Response(status=200)

'''
process_cer

Process a contextElementResponse XML element
'''
def process_cer(cer):
    app.logger.info("Processing contextElementResponse")
    entity = get_entity(cer)
    id = effective_string(entity['id'])
    type = effective_string(entity['type'])
    app.logger.info('   entity id:   <' + entity['id'] + '> (effective: <' + id + '>')
    app.logger.info('   entity type: <' + entity['type'] + '> (effective: <' + type + '>)')
    # Process contextAttribute list
    for ca in cer.findall('.//contextAttribute'):
        process_ca(ca, id, type)

'''
get_entity

Parses XML to find entity, which is returned as a dict
(keys are 'id' and 'type')
'''
def get_entity(doc):

    r = {}
    entity_tag = doc.find('.//entityId')
    r['id'] = entity_tag.find('id').text
    r['type'] = entity_tag.attrib.get('type')
    return r

'''
process_ca

Process a contextAttribute XML element
'''
def process_ca(ca, entity_id, entity_type):

    name = ca.find('name').text
    raw_type = ca.find('type').text
    value = ca.find('contextValue').text

    if (raw_type == None):
        type = ''

    type = effective_string(raw_type)

    app.logger.info('   attr name:  <' + name + '>')
    app.logger.info('   attr type:  <' + raw_type + '> (effective: <' + type + '>)')

    if value == None:
        app.logger.info('   value is None, nothing to do')
    else:
        app.logger.info('   attr value: <' + value + '>')
        persists(entity_id, entity_type, name, type, value)

'''
efective_string

Take into account weird characters (such as ':' and '-') and scape it to produce the
final string that will go into URLs and filnames
'''
def effective_string(s):
    # FIXME: currently we limit to replace weird characters with "_". As side effect, there could be ambiguities in
    # some cases (e.g. "rare-type" and "rare:type" are translated  to the same "rare_type"), a better implementation
    # would actually scape the characters
    return re.sub(r'[-:]', '_', s)


'''
persists

Record the attribute identified by the tuple (entity_id, entity_type, attr_name, attr_type)
in the HDFS layer
'''
def persists(entity_id, entity_type, attr_name, attr_type, attr_value):
    file_name = entity_id + '-' + entity_type + '-' + attr_name + '-' + attr_type + '.txt'

    date = datetime.now()
    date_timestamp = date.strftime('%s')
    date_pretty = date.isoformat()

    line = date_pretty + delimiter + date_timestamp + delimiter + entity_id + delimiter + entity_type + delimiter + attr_name + delimiter + attr_type + delimiter + attr_value
    app.logger.info('   appending to ' + file_name + ': ' + line)
    line += '\n'
    try:
        app.config['HDFS_BACKEND'].cosmos_append(file_name, line)
        app.logger.info('   append OK')
    except Timeout:
        app.logger.info('Exception: Timeout expired')
    except ConnectionError, e:
        app.logger.info('Exception: Connection error <' + str(e) + '>')
    except Exception, e:
        app.logger.info('Exception: <' + str(e) + '>')


if __name__ == '__main__':

    if not log_off:
        # Remove all previous handerls in logger, then register handler with the format we want
        for h in app.logger.handlers:
            app.logger.removeHandler(h)
        h = logging.FileHandler('ngsi2cosmos' + str(port) + '.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        h.setFormatter(formatter)
        # Set the following line to either logging.INFO or logging.DEBUG
        h.setLevel(logging.DEBUG)
        app.logger.addHandler(h)

    if hdfs_backend == 'HttpFS':
        app.logger.info('Using HttpFS backend')
        app.config['HDFS_BACKEND'] = HttpFsBackend(app.logger, cosmos_url, actual_base_dir, cosmos_user)
    else:   # WebHDFS
        app.logger.info('Using WebHDFS backend')
        app.config['HDFS_BACKEND'] = WebHdfsBackend(app.logger, cosmos_url, actual_base_dir, cosmos_user, dn_map)

    # Create the target HDFS directory where the data is going to be stored, if not existing yet
    try:
        app.config['HDFS_BACKEND'].cosmos_create_base_dir()
        app.logger.info('   create HDFS base dir OK')
    except Timeout:
        app.logger.info('Exception: Timeout expired')
    except ConnectionError, e:
        app.logger.info('Exception: Connection error <' + str(e) + '>')
    except Exception, e:
        app.logger.info('Exception: <' + str(e) + '>')
 
    # Parse the cosmos URL in order to obtain the host
    cosmos_host = cosmos_url.split("//")[1].split(":")[0]

    # Compose the table name
    table_name = cosmos_user + actual_base_dir.split(cosmos_user)[1].replace("/", "_")

    # Create the Hive external table
    hiveClient = HiveClient(cosmos_host, 10000);
    hiveClient.open_connection()
    hiveClient.create_table("create external table if not exists " + table_name + " (ts string, ts_ms int, " \
	"entity_name string, entity_type string, attribute_name string, attribute_type string, value string) " \
	"row format delimited fields terminated by '|' location '" + actual_base_dir + "'")
    hiveClient.close_connection()
    app.logger.info('   create Hive table OK')

    # Run the server
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True)

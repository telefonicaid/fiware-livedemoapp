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
from requests import post, Timeout, ConnectionError
import logging
import json
from datetime import datetime
from sys import argv

from xml_request import query_issues_xml, update_issue_xml, update_issue_severity_xml
from constants import *

from env import cb_url, store_url

# Default arguments
port = 5000
default_timeout = 3
acc_token_file = 'accounting_token.json'

# Arguments from command line
if len(argv) > 3:
    port = int(argv[1])
    cb_url = argv[2]
    store_url = argv[3]

app = Flask(__name__)

@app.route('/set_accounting', methods=['POST'])
def set_accounting():
    set_correlation(1)
    app.logger.info('====================================================')
    app.logger.info('Set accounting')
    app.logger.info(request.json)
    f = open(acc_token_file, 'w')
    f.write(json.dumps(request.json, sort_keys=True, indent=4, separators=(',', ': ')))
    return Response(status=200)


@app.route('/new_issue/<affected_entity_id>/<type>/<severity>', methods=['POST'])
def new_issue(affected_entity_id, type, severity):
    app.logger.info('====================================================')
    
    event_attrs = {}
    event_attrs[EVENT_AFFECTED_ENTITY_ID] = affected_entity_id 
    event_attrs[EVENT_EVENT_TYPE] = type
    event_attrs[EVENT_EVENT_SEVERITY] = severity
    
    issue = str(next_issue_id())
    create_issue(issue, event_attrs)

    #return Response(status=200)
    return "Issue" + issue


@app.route('/set_counter/<n>', methods=['POST'])
def set_counter(n):
    global issue_counter
    app.logger.info('====================================================')
    try:
        issue_counter = int(n)
        app.logger.info('Issue counter set to ' + str(issue_counter))
    except ValueError:
        app.logger.info('Invalid integer: ' + n)

    return Response(status=200)


@app.route('/set_correlation/<n>', methods=['POST'])
def set_correlation(n):
    global correlation
    app.logger.info('====================================================')
    try:
        correlation = int(n)
        app.logger.info('Correlation set to ' + str(correlation))
    except ValueError:
        app.logger.info('Invalid integer: ' + n)

    return Response(status=200)


@app.route('/notify', methods=['POST'])
def process_notify():

    app.logger.info('====================================================')

    if (len(request.data) == 0):
        app.logger.info('Empty notification message')
        return Response(status=200)

    app.logger.debug('New notification (raw): \n' + request.data)

    notify_context = etree.fromstring(request.data)

    entity = get_entity(notify_context)
    app.logger.info('entity ID:   ' + entity['id'])
    app.logger.info('entity Type: ' + entity['type'])

    if ((entity['id'] != 'CEPEventReporter_Singleton') or(entity['type'] != 'CEPEventReporter')):
        app.logger.info('Notification not corresponding to CEP event')
        return Response(status=200)

    event_attrs = get_attributes(notify_context)
    for attr in event_attrs.keys():
        app.logger.info('event attribute ' + attr + ': ' + event_attrs[attr])

    if not validate_event_attrs(event_attrs):
        app.logger.info("missing required attributes in Event")
        return Response(status=200)

    issue_id = match_issue(event_attrs)
    if issue_id == None:
        create_issue(str(next_issue_id()), event_attrs)
    else:
        update_issue(issue_id, event_attrs)

    return Response(status=200)

'''
get_entity

Parses XML document to find entity, which is returned as a dict
(keys are 'id' and 'type')
'''
def get_entity(doc):

    r = {}

    entity_tag = doc.find('.//entityId')
    r['id'] = entity_tag.find('id').text
    r['type'] = entity_tag.attrib.get('type')

    return r

'''
get_attributes

Parses XML document to find attributes, which are returned
as a dict (keys are attribute name and values are attribute values)
'''
def get_attributes(doc):

    r = {}

    for ca in doc.findall('.//contextAttribute'):
        name = ca.find('name').text
        value = ca.find('contextValue').text
        if (value != None):
            r[name] = value

    return r

'''
match_issue

queryContext contextBroker for Issue entities and returns the
entity id of the matching entity in the case of successful matching.
Otherwise it return None
'''
def match_issue(event_attrs):

    try:
        response = do_post(cb_url + 'NGSI10/queryContext', query_issues_xml()).content
        app.logger.info('response OK')
        app.logger.debug(response)
        
    except Timeout:
        app.logger.info('Timeout expired!')
        return None

    except ConnectionError:
        app.logger.info('Connection error!')
        return None


    query_result = etree.fromstring(response)

    # Note that this work also when no issue is found, as the error message in that case doesn't
    # include any contextElement so the loop is empty
    for ce in query_result.findall('.//contextElement'):

        issue_id = get_entity(ce)['id']
        issue_attrs = get_attributes(ce)

        app.logger.info('Checking ' + issue_id)
        for attr in issue_attrs.keys():
            app.logger.info('issue attribute ' + attr + ': ' + issue_attrs[attr])

        # Matching rule is:
        #    issue.ISSUE_AFFECTED_ID == event.EVENT_AFFECTED_ENTITY_ID &&
        #    issue.ISSUE_ISSUE_TYPE == event.EVENT_EVENT_TYPE &&
        #    issue.ISSUE_CLOSING_DATE == EMPTY_CONTENT

        # Sanity check
        if not validate_issue_attrs(issue_attrs):
            app.logger.info("missing required attributes in Issue")
            continue

        issue_affected_id = issue_attrs[ISSUE_AFFECTED_ID]
        issue_type = issue_attrs[ISSUE_ISSUE_TYPE]
        issue_closing_date = issue_attrs[ISSUE_CLOSING_DATE]
        event_affected_id = event_attrs[EVENT_AFFECTED_ENTITY_ID]
        event_type = event_attrs[EVENT_EVENT_TYPE]

        app.logger.info('check: '
                        + issue_affected_id + ' == ' + event_affected_id + ' and '
                        + issue_type + ' == ' + event_type + ' and '
                        + issue_closing_date + ' == ' + EMPTY_CONTENT + ' ?')

        if (issue_affected_id == event_affected_id and
            issue_type == event_type and
            issue_closing_date == EMPTY_CONTENT):
            app.logger.info('match!')
            return issue_id

    return None

'''
validate_issue_attrs

Check that all the needed keys in an attribute dict for Issue are there
'''
def validate_issue_attrs(attrs):

    return (attrs.has_key(ISSUE_AFFECTED_ID) and attrs.has_key(ISSUE_ISSUE_TYPE)
            and attrs.has_key(ISSUE_CLOSING_DATE))

'''
validate_event_attrs

Check that all the needed keys in an attribute dict for Event are there
'''
def validate_event_attrs(attrs):

    return (attrs.has_key(EVENT_AFFECTED_ENTITY_ID) and attrs.has_key(EVENT_EVENT_TYPE)
            and attrs.has_key(EVENT_EVENT_SEVERITY))

'''
create_issue

Creates issue using registerContext
'''
def create_issue(issue_id, event_attrs):

    try:
        app.logger.info('Creating Issue ID ' + issue_id)

        update_xml = update_issue_xml(issue_id, event_attrs[EVENT_AFFECTED_ENTITY_ID], event_attrs[EVENT_EVENT_TYPE],
                                  event_attrs[EVENT_EVENT_SEVERITY], 'APPEND')
        response = do_post(cb_url + 'NGSI10/updateContext', update_xml).content
        app.logger.info('response OK')
        app.logger.debug(response)
    
        do_account()

    except Timeout:
        app.logger.info('Timeout expired!')

    except ConnectionError:
        app.logger.info('Connection error!')


'''
do_account

Send a record to accounting system
'''
def do_account():
    global correlation

    #Read authentication token
    f = open(acc_token_file, 'r')
    acc_token = json.loads(f.read())

    # Build payload
    acc = {}
    acc['offering'] = acc_token['offering']
    acc['customer'] = acc_token['customer']
    acc['correlation_number'] = correlation
    acc['time_stamp'] = datetime.now().isoformat()
    acc['record_type'] = 'event'
    acc['value'] = 1
    acc['unit'] = 'issue'

    correlation += 1

    #Sending
    app.logger.info('sending accounting information: ' + json.dumps(acc, sort_keys=True, indent=4, separators=(',', ': ')))
    headers = {}
    headers['Content-Type'] = 'application/json'
    app.logger.info('Sending POST to: ' + store_url + '/api/contracting/' + acc_token['reference'] + '/accounting')
    try:
        response = post(store_url + '/api/contracting/' + acc_token['reference'] + '/accounting', json.dumps(acc), headers=headers, timeout=default_timeout)
        app.logger.info('response OK')
        app.logger.debug(response)
    except Timeout:
        app.logger.info('Timeout expired!')
    except ConnectionError:
        app.logger.info('Connection error!')


'''
update_issue

Update existing Issue with Event information
'''
def update_issue(issue_id, event_attrs):

    app.logger.info('Update issue ' + issue_id)
    update_xml = update_issue_severity_xml(issue_id, event_attrs[EVENT_EVENT_SEVERITY])
    app.logger.debug(update_xml)
    try:
        response = do_post(cb_url + 'NGSI10/updateContext', update_xml).content
        app.logger.info('response OK')
        app.logger.debug(response)
    except Timeout:
        app.logger.info('Timeout expired!')
    except ConnectionError:
        app.logger.info('Connection error!')


'''
do_post

This is a wrapper of requests module post method, but ensuring that the
Content-Type is what we need
'''
def do_post(url, data):

    # Setting the content-type is important: otherwise ContextBroker will don't process the request
    headers = {}
    headers['Content-Type'] = 'application/xml'
    app.logger.info('Sending POST to: ' + url)
    return post(url, data, headers=headers, timeout=default_timeout)

'''
next_issue_id

Returns next available Issue ID and update global counter
'''
def next_issue_id():

    global issue_counter

    r = issue_counter
    issue_counter += 1

    return r

if __name__ == '__main__':

    # Remove all previous handerls in logger, then register handler with the format we want
    for h in app.logger.handlers:
        app.logger.removeHandler(h)
    h = logging.FileHandler('event2issue.log')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    h.setFormatter(formatter)
    h.setLevel(logging.INFO)
    app.logger.addHandler(h)

    # Set up initial issue counter and accounting correlation
    issue_counter = 1
    correlation = 1

    # Run the server
    app.run(host='0.0.0.0', port=port, debug=True)

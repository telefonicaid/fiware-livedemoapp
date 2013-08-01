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

from datetime import datetime
from constants import EMPTY_CONTENT

def query_issues_xml():

    s = ''
    s += '<?xml version="1.0" encoding="UTF-8"?>\n'
    s += '  <queryContextRequest>\n'
    s += '    <entityIdList>\n'
    s += '      <entityId type="Issue" isPattern="true">\n'
    s += '        <id>.*</id>\n'
    s += '      </entityId>\n'
    s += '    </entityIdList>\n'
    s += '    <attributeList>\n'
    s += '    </attributeList>\n'
    s += '  </queryContextRequest>\n'
    return s

def register_issue_xml(id):

    s = ''
    s += '<?xml version="1.0"?>\n'
    s += '  <registerContextRequest>\n'
    s += '    <contextRegistrationList>\n'
    s += '      <contextRegistration>\n'
    s += '        <entityIdList>\n'
    s += '          <entityId type="Issue" isPattern="false">\n'
    s += '            <id>Issue' + id + '</id>\n'
    s += '          </entityId>\n'
    s += '        </entityIdList>\n'
    s += '        <contextRegistrationAttributeList>\n'
    s += '          <contextRegistrationAttribute>\n'
    s += '            <name>severity</name>\n'
    s += '            <type>string</type>\n'
    s += '            <isDomain>false</isDomain>\n'
    s += '          </contextRegistrationAttribute>\n'
    s += '          <contextRegistrationAttribute>\n'
    s += '            <name>affectedId</name>\n'
    s += '            <type>string</type>\n'
    s += '            <isDomain>false</isDomain>\n'
    s += '          </contextRegistrationAttribute>\n'
    s += '          <contextRegistrationAttribute>\n'
    s += '            <name>technician</name>\n'
    s += '            <type>string</type>\n'
    s += '            <isDomain>false</isDomain>\n'
    s += '          </contextRegistrationAttribute>\n'
    s += '          <contextRegistrationAttribute>\n'
    s += '            <name>description</name>\n'
    s += '            <type>string</type>\n'
    s += '            <isDomain>false</isDomain>\n'
    s += '          </contextRegistrationAttribute>\n'
    s += '          <contextRegistrationAttribute>\n'
    s += '            <name>coordinates</name>\n'
    s += '            <type>string</type>\n'
    s += '            <isDomain>false</isDomain>\n'
    s += '          </contextRegistrationAttribute>\n'
    s += '          <contextRegistrationAttribute>\n'
    s += '            <name>issueType</name>\n'
    s += '            <type>string</type>\n'
    s += '            <isDomain>false</isDomain>\n'
    s += '          </contextRegistrationAttribute>\n'
    s += '          <contextRegistrationAttribute>\n'
    s += '            <name>creationDate</name>\n'
    s += '            <type>string</type>\n'
    s += '            <isDomain>false</isDomain>\n'
    s += '          </contextRegistrationAttribute>\n'
    s += '          <contextRegistrationAttribute>\n'
    s += '            <name>closingDate</name>\n'
    s += '            <type>string</type>\n'
    s += '            <isDomain>false</isDomain>\n'
    s += '          </contextRegistrationAttribute>\n'
    s += '          <contextRegistrationAttribute>\n'
    s += '            <name>imageFile</name>\n'
    s += '            <type>string</type>\n'
    s += '            <isDomain>false</isDomain>\n'
    s += '          </contextRegistrationAttribute>\n'
    s += '        </contextRegistrationAttributeList>\n'
    s += '        <providingApplication>http://www.fi-ware.eu/NGSI/dummy</providingApplication>\n'
    s += '      </contextRegistration>\n'
    s += '    </contextRegistrationList>\n'
    s += '    <duration>P1Y</duration>\n'
    s += '  </registerContextRequest>\n'
    return s

def update_issue_xml(id, affected_entity, alarm_type, severity):

    s = ''
    s += '<?xml version="1.0" encoding="UTF-8"?>\n'
    s += '<updateContextRequest>\n'
    s += '  <contextElementList>\n'
    s += '    <contextElement>\n'
    s += '      <entityId type="Issue" isPattern="false">\n'
    s += '	      <id>Issue' + id + '</id>\n'
    s += '	    </entityId>\n'
    s += '      <contextAttributeList>\n'
    s += '        <contextAttribute>\n'
    s += '          <name>affectedId</name>\n'
    s += '          <type>string</type>\n'
    s += '          <contextValue>' + affected_entity + '</contextValue>\n'
    s += '        </contextAttribute>\n'
    s += '        <contextAttribute>\n'
    s += '          <name>issueType</name>\n'
    s += '          <type>string</type>\n'
    s += '          <contextValue>' + alarm_type + '</contextValue>\n'
    s += '        </contextAttribute>\n'
    s += '        <contextAttribute>\n'
    s += '          <name>severity</name>\n'
    s += '          <type>string</type>\n'
    s += '          <contextValue>' + severity + '</contextValue>\n'
    s += '        </contextAttribute>\n'
    s += '        <contextAttribute>\n'
    s += '          <name>description</name>\n'
    s += '          <type>string</type>\n'
    s += '          <contextValue>' + severity + '</contextValue>\n'
    s += '        </contextAttribute>\n'
    s += '        <contextAttribute>\n'
    s += '          <name>creationDate</name>\n'
    s += '          <type>string</type>\n'
    s += '          <contextValue>' + datetime.now().isoformat() + '</contextValue>\n'
    s += '        </contextAttribute>\n'
    s += '        <contextAttribute>\n'
    s += '          <name>closingDate</name>\n'
    s += '          <type>string</type>\n'
    s += '          <contextValue>' + EMPTY_CONTENT + '</contextValue>\n'
    s += '        </contextAttribute>\n'
    s += '        <contextAttribute>\n'
    s += '          <name>imageFile</name>\n'
    s += '          <type>string</type>\n'
    s += '          <contextValue>' + EMPTY_CONTENT + '</contextValue>\n'
    s += '        </contextAttribute>\n'
    s += '      </contextAttributeList>\n'
    s += '    </contextElement>\n'
    s += '  </contextElementList>\n'
    s += '  <updateAction>UPDATE</updateAction>\n'
    s += '</updateContextRequest>\n'
    return s

def update_issue_severity_xml(id, severity):

    s = ''
    s += '<?xml version="1.0" encoding="UTF-8"?>\n'
    s += '<updateContextRequest>\n'
    s += '  <contextElementList>\n'
    s += '    <contextElement>\n'
    s += '      <entityId type="Issue" isPattern="false">\n'
    s += '	      <id>' + id + '</id>\n'
    s += '	    </entityId>\n'
    s += '      <contextAttributeList>\n'
    s += '        <contextAttribute>\n'
    s += '          <name>severity</name>\n'
    s += '          <type>string</type>\n'
    s += '          <contextValue>' + severity + '</contextValue>\n'
    s += '        </contextAttribute>\n'
    s += '      </contextAttributeList>\n'
    s += '    </contextElement>\n'
    s += '  </contextElementList>\n'
    s += '  <updateAction>UPDATE</updateAction>\n'
    s += '</updateContextRequest>\n'
    return s

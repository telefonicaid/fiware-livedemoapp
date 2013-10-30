#!/bin/bash
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

(curl ${CB_HOST}:${CB_PORT}/NGSI9/subscribeContextAvailability -s -S --header 'Content-Type: application/xml' -d @- | xmllint --format - ) <<EOF
<?xml version="1.0"?>
<subscribeContextAvailabilityRequest>
  <entityIdList>
        <entityId type="Issue" isPattern="true">
          <id>Issue.*</id>
        </entityId>
  </entityIdList>
  <attributeList>
 </attributeList>
  <reference>http://${FED_CB_HOST}:${FED_CB_PORT}/ngsi9/notifyContextAvailability</reference>
  <duration>P1Y</duration>
</subscribeContextAvailabilityRequest>
EOF

(curl ${CB_HOST}:${CB_PORT}/NGSI10/subscribeContext -s -S --header 'Content-Type: application/xml' -d @- | xmllint --format - ) <<EOF
<?xml version="1.0"?>
<subscribeContextRequest>
  <entityIdList>
        <entityId type="Issue" isPattern="true">
          <id>Issue.*</id>
        </entityId>
  </entityIdList>
  <attributeList>
 </attributeList>
  <reference>http://${FED_CB_HOST}:${FED_CB_PORT}/ngsi10/notifyContext</reference>
  <duration>P1Y</duration>
  <notifyConditions>
        <notifyCondition>
          <type>ONCHANGE</type>
          <condValueList>
                <condValue>severity</condValue>
                <condValue>affectedId</condValue>
                <condValue>technician</condValue>
                <condValue>description</condValue>
                <condValue>coordinates</condValue>
                <condValue>issueType</condValue>
                <condValue>creationDate</condValue>
                <condValue>closingDate</condValue>
                <condValue>imageFile</condValue>
        </condValueList>
        </notifyCondition>
  </notifyConditions>
</subscribeContextRequest>
EOF

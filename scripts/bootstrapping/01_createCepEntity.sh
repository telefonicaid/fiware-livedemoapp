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

(curl ${CB_HOST}:${CB_PORT}/NGSI10/updateContext -s -S --header 'Content-Type: application/xml' -d @- | xmllint --format -) <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<updateContextRequest>
  <contextElementList>
     <contextElement>
        <entityId type="CEPEventReporter" isPattern="false">
          <id>CEPEventReporter_Singleton</id>
        </entityId>
        <contextAttributeList>
          <contextAttribute>
            <name>Name</name>
            <type>string</type>
            <contextValue>-</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>OccurrenceTime</name>
            <type>string</type>
            <contextValue>-</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>DetectionTime</name>
            <type>string</type>
            <contextValue>-</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>Duration</name>
            <type>string</type>
            <contextValue>-</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>Certainty</name>
            <type>string</type>
            <contextValue>-</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>Cost</name>
            <type>string</type>
            <contextValue>-</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>Annotation</name>
            <type>string</type>
            <contextValue>-</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>EventId</name>
            <type>string</type>
            <contextValue>-</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>EventSource</name>
            <type>string</type>
            <contextValue>-</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>TimeInstant</name>
            <type>string</type>
            <contextValue>-</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>AffectedEntity</name>
            <type>string</type>
            <contextValue>-</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>AffectedEntityType</name>
            <type>string</type>
            <contextValue>-</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>EventType</name>
            <type>string</type>
            <contextValue>-</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>EventSeverity</name>
            <type>string</type>
            <contextValue>-</contextValue>
          </contextAttribute>
        </contextAttributeList>
      </contextElement>
  </contextElementList>
  <updateAction>APPEND</updateAction>
</updateContextRequest>
EOF

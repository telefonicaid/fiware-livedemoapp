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

(curl ${CB_HOST}:${CB_PORT}/NGSI10/subscribeContext -s -S --header 'Content-Type: application/xml' -d @- | xmllint --format - ) <<EOF
<?xml version="1.0"?>
<subscribeContextRequest>
  <entityIdList>
        <entityId type="Node" isPattern="true">
          <id>OUTSMART.NODE.*</id>
        </entityId>
        <entityId type="AMMS" isPattern="true">
          <id>OUTSMART.AMMS.*</id>
        </entityId>
        <entityId type="Regulator" isPattern="true">
          <id>OUTSMART.RG.*</id>
        </entityId>
  </entityIdList>
  <attributeList>
 </attributeList>
  <reference>http://${CYGNUS_HOST}:${CYGNUS_PORT}/notify</reference>
  <duration>P1Y</duration>
  <notifyConditions>
        <notifyCondition>
          <type>ONCHANGE</type>
          <condValueList>
                <condValue>TimeInstant</condValue>
        </condValueList>
        </notifyCondition>
  </notifyConditions>
  <!--use throttling only if you expect too verbose context producer -->
  <!--throttling>PT5S</throttling-->
</subscribeContextRequest>
EOF

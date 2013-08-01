#!/bin/bash
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

(curl localhost:1026/NGSI10/updateContext -s -S --header 'Content-Type: application/xml' -d @- | xmllint --format - ) <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<updateContextRequest>
  <contextElementList>
    <contextElement>
      <entityId type="Van" isPattern="false">
        <id>van1</id>
      </entityId>
      <contextAttributeList>
        <contextAttribute>
          <name>current_position</name>
          <contextValue>43.475579, -3.804835</contextValue>
        </contextAttribute>
      </contextAttributeList>
    </contextElement>
    <contextElement>
      <entityId type="Van" isPattern="false">
        <id>van2</id>
      </entityId>
      <contextAttributeList>
        <contextAttribute>
          <name>current_position</name>
          <contextValue>43.472823, -3.790823</contextValue>
        </contextAttribute>
      </contextAttributeList>
    </contextElement>
    <contextElement>
      <entityId type="Van" isPattern="false">
        <id>van3</id>
      </entityId>
      <contextAttributeList>
        <contextAttribute>
          <name>current_position</name>
          <contextValue>43.478148, -3.804234</contextValue>
        </contextAttribute>
      </contextAttributeList>
    </contextElement>
    <contextElement>
      <entityId type="Van" isPattern="false">
        <id>van4</id>
      </entityId>
      <contextAttributeList>
        <contextAttribute>
          <name>current_position</name>
          <contextValue>43.472044, -3.79505</contextValue>
        </contextAttribute>
      </contextAttributeList>
    </contextElement>
  </contextElementList>
  <updateAction>Update</updateAction>
</updateContextRequest>
EOF

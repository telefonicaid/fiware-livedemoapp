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

(curl ${CB_HOST}:${CB_PORT}/NGSI9/registerContext -s -S --header 'Content-Type: application/xml' -d @- | xmllint --format - ) <<EOF
<?xml version="1.0"?>
  <registerContextRequest>
    <contextRegistrationList>
      <contextRegistration>
        <entityIdList>
          <entityId type="Van" isPattern="false">
            <id>van1</id>
          </entityId>
          <entityId type="Van" isPattern="false">
            <id>van2</id>
          </entityId>
          <entityId type="Van" isPattern="false">
            <id>van3</id>
          </entityId>
          <entityId type="Van" isPattern="false">
            <id>van4</id>
          </entityId>
        </entityIdList>
        <contextRegistrationAttributeList>
          <contextRegistrationAttribute>
            <name>current_position</name>
            <type></type>
            <isDomain>false</isDomain>
          </contextRegistrationAttribute>
        </contextRegistrationAttributeList>
        <providingApplication>http://www.fi-ware.eu/NGSI/dummy</providingApplication>
      </contextRegistration>
    </contextRegistrationList>
    <duration>P5Y</duration>
  </registerContextRequest>
EOF

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
        <entityId type="Technician" isPattern="false">
          <id>tech1</id>
        </entityId>
        <contextAttributeList>
          <contextAttribute>
            <name>name</name>
            <type>string</type>
            <contextValue></contextValue>
            <contextValue>Marcos Lorenzo Fernandez</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>working_area</name>
            <type>string</type>
            <contextValue>28050</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>function</name>
            <type>string</type>
            <contextValue>Worker</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>mobile_phone</name>
            <type>string</type>
            <contextValue>$1</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>email</name>
            <type>string</type>
            <contextValue>marcos.lorenzo@smartcitylights.com</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>twitter</name>
            <type>string</type>
            <contextValue>mLorenzo</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>van</name>
            <type>string</type>
            <contextValue>van2</contextValue>
          </contextAttribute>
        </contextAttributeList>
      </contextElement>
  </contextElementList>
  <updateAction>Update</updateAction>
</updateContextRequest>
EOF

(curl ${CB_HOST}:${CB_PORT}/NGSI10/updateContext -s -S --header 'Content-Type: application/xml' -d @- | xmllint --format -) <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<updateContextRequest>
  <contextElementList>
     <contextElement>
        <entityId type="Technician" isPattern="false">
          <id>tech2</id>
        </entityId>
        <contextAttributeList>
          <contextAttribute>
            <name>name</name>
            <type>string</type>
            <contextValue></contextValue>
            <contextValue>Milan De Vos</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>working_area</name>
            <type>string</type>
            <contextValue>28050</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>function</name>
            <type>string</type>
            <contextValue>Worker</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>mobile_phone</name>
            <type>string</type>
            <contextValue>$2</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>email</name>
            <type>string</type>
            <contextValue>milan.devos@smartcitylights.com</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>twitter</name>
            <type>string</type>
            <contextValue>mDeVos</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>van</name>
            <type>string</type>
            <contextValue>van4</contextValue>
          </contextAttribute>
        </contextAttributeList>
      </contextElement>
  </contextElementList>
  <updateAction>Update</updateAction>
</updateContextRequest>
EOF

(curl ${CB_HOST}:${CB_PORT}/NGSI10/updateContext -s -S --header 'Content-Type: application/xml' -d @- | xmllint --format -) <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<updateContextRequest>
  <contextElementList>
     <contextElement>
        <entityId type="Technician" isPattern="false">
          <id>tech3</id>
        </entityId>
        <contextAttributeList>
          <contextAttribute>
            <name>name</name>
            <type>string</type>
            <contextValue></contextValue>
            <contextValue>Maria Perez Perea</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>working_area</name>
            <type>string</type>
            <contextValue>28050</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>function</name>
            <type>string</type>
            <contextValue>Worker</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>mobile_phone</name>
            <type>string</type>
            <contextValue>$3</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>email</name>
            <type>string</type>
            <contextValue>maria.perez@smartcitylights.com</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>twitter</name>
            <type>string</type>
            <contextValue>mPerez</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>van</name>
            <type>string</type>
            <contextValue>van3</contextValue>
          </contextAttribute>
        </contextAttributeList>
      </contextElement>
  </contextElementList>
  <updateAction>Update</updateAction>
</updateContextRequest>
EOF

(curl ${CB_HOST}:${CB_PORT}/NGSI10/updateContext -s -S --header 'Content-Type: application/xml' -d @- | xmllint --format -) <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<updateContextRequest>
  <contextElementList>
     <contextElement>
        <entityId type="Technician" isPattern="false">
          <id>tech4</id>
        </entityId>
        <contextAttributeList>
          <contextAttribute>
            <name>name</name>
            <type>string</type>
            <contextValue></contextValue>
            <contextValue>Jacinto Salas Torres</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>working_area</name>
            <type>string</type>
            <contextValue>28050</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>function</name>
            <type>string</type>
            <contextValue>Worker</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>mobile_phone</name>
            <type>string</type>
            <contextValue>$4</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>email</name>
            <type>string</type>
            <contextValue>jacinto.salas@smartcitylights.com</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>twitter</name>
            <type>string</type>
            <contextValue>mJSalas</contextValue>
          </contextAttribute>
          <contextAttribute>
            <name>van</name>
            <type>string</type>
            <contextValue>van1</contextValue>
          </contextAttribute>
        </contextAttributeList>
      </contextElement>
  </contextElementList>
  <updateAction>Update</updateAction>
</updateContextRequest>
EOF

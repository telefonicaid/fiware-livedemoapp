# Copyright 2014 Telefonica Investigación y Desarrollo, S.A.U
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

curl --request POST ${CB_HOST}:${CB_PORT}/ngsi10/updateContext  --header 'Content-Type: application/xml' $CURL_VERBOSE --data-binary @ngsi_cre_regulador_1.xml



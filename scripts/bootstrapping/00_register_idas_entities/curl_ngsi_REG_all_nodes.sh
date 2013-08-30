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

PORT=1026

curl --request POST  http://0.0.0.0:$PORT/ngsi9/registerContext  --header 'Content-Type: application/xml' $CURL_VERBOSE --data-binary @ngsi_reg_node_3500.xml

sleep 1
curl --request POST  http://0.0.0.0:$PORT/ngsi9/registerContext  --header 'Content-Type: application/xml' $CURL_VERBOSE --data-binary @ngsi_reg_node_3501.xml

sleep 1
curl --request POST  http://0.0.0.0:$PORT/ngsi9/registerContext  --header 'Content-Type: application/xml' $CURL_VERBOSE --data-binary @ngsi_reg_node_3502.xml

sleep 1
curl --request POST  http://0.0.0.0:$PORT/ngsi9/registerContext  --header 'Content-Type: application/xml' $CURL_VERBOSE --data-binary @ngsi_reg_node_3503.xml

sleep 1
curl --request POST  http://0.0.0.0:$PORT/ngsi9/registerContext  --header 'Content-Type: application/xml' $CURL_VERBOSE --data-binary @ngsi_reg_node_3504.xml

sleep 1
curl --request POST  http://0.0.0.0:$PORT/ngsi9/registerContext  --header 'Content-Type: application/xml' $CURL_VERBOSE --data-binary @ngsi_reg_node_3505.xml

sleep 1
curl --request POST  http://0.0.0.0:$PORT/ngsi9/registerContext  --header 'Content-Type: application/xml' $CURL_VERBOSE --data-binary @ngsi_reg_node_3506.xml

sleep 1
curl --request POST  http://0.0.0.0:$PORT/ngsi9/registerContext  --header 'Content-Type: application/xml' $CURL_VERBOSE --data-binary @ngsi_reg_node_3507.xml

sleep 1
curl --request POST  http://0.0.0.0:$PORT/ngsi9/registerContext  --header 'Content-Type: application/xml' $CURL_VERBOSE --data-binary @ngsi_reg_node_3508.xml

sleep 1
curl --request POST  http://0.0.0.0:$PORT/ngsi9/registerContext  --header 'Content-Type: application/xml' $CURL_VERBOSE --data-binary @ngsi_reg_node_3509.xml

sleep 1
curl --request POST  http://0.0.0.0:$PORT/ngsi9/registerContext  --header 'Content-Type: application/xml' $CURL_VERBOSE --data-binary @ngsi_reg_node_3510.xml

sleep 1
curl --request POST  http://0.0.0.0:$PORT/ngsi9/registerContext  --header 'Content-Type: application/xml' $CURL_VERBOSE --data-binary @ngsi_reg_node_3511.xml

sleep 1
curl --request POST  http://0.0.0.0:$PORT/ngsi9/registerContext  --header 'Content-Type: application/xml' $CURL_VERBOSE --data-binary @ngsi_reg_node_3512.xml


sleep 1
curl --request POST  http://0.0.0.0:$PORT/ngsi9/registerContext  --header 'Content-Type: application/xml' $CURL_VERBOSE --data-binary @ngsi_reg_node_3513.xml

sleep 1
curl --request POST  http://0.0.0.0:$PORT/ngsi9/registerContext  --header 'Content-Type: application/xml' $CURL_VERBOSE --data-binary @ngsi_reg_node_3514.xml

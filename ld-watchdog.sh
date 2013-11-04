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

# This watchdog script can be used to test that a LiveDemoApp installation is
# properly configured. In FI-WARE we configure cron to run this script each midnight and
# send a report by email
#
# Notes to take into account:
#
# - This scripts assumes that the fiware-livedemoapp repository is installed in /home/test2.
#   Otherwise, just change the LDAPP_DIR variable at the beggining of the script
# - We have our environment in myEnv.sh in the scripts/ directory. You can do a 
#   symlink myENV.sh -> ENV.sh to make things easier
# - The script also assumes that you have the following scripts configured in /usr/local/bin:
#   monit_log_processing.py, garbage-collector.py and lastest-updates.py, that can be found in 
#   the Orion Context Broker repo at https://github.com/telefonicaid/fiware-orion (the recommended 
#   way is to install that repo wherever you want in your system, then symlink the scripts from
#   /usr/local/bin) 
# - It assumes that contextBroker runs in localhost (i.e. CB_HOST=localhost)

DB=orion
LDAPP_DIR=/home/test2/fiware-livedemoapp
SCRIPTS_DIR=$LDAPP_DIR/scripts
. $SCRIPTS_DIR/myENV.sh

function printVans() {
   VAN1=$(./get-van.py  | grep 'current_position' | sed -n '1p' | awk -F ':' '{print $2'} | tr -d ' ')
   VAN2=$(./get-van.py  | grep 'current_position' | sed -n '2p' | awk -F ':' '{print $2'} | tr -d ' ')
   VAN3=$(./get-van.py  | grep 'current_position' | sed -n '3p' | awk -F ':' '{print $2'} | tr -d ' ')
   VAN4=$(./get-van.py  | grep 'current_position' | sed -n '4p' | awk -F ':' '{print $2'} | tr -d ' ')
   echo -e "$VAN1\t$VAN2\t$VAN3\t$VAN4"
}

function databaseCount() {
   REG_N=$(mongo orion --quiet --eval "db.registrations.count()")
   ENT_N=$(mongo orion --quiet --eval "db.entities.count()")
   CSUB_N=$(mongo orion --quiet --eval "db.csubs.count()")
   CASUB_N=$(mongo orion --quiet --eval "db.casubs.count()")
   ASSOC_N=$(mongo orion --quiet --eval "db.associations.count()")

   echo "+ registrations collection count: $REG_N"
   echo "+ entities collection count:      $ENT_N"
   echo "+ csubs collection count:         $CSUB_N"
   echo "+ casubs collection count:        $CASUB_N"
   echo "+ associations collection count:  $ASSOC_N"
}

echo "=========="
echo "Statistics"
echo "=========="
curl -s ${CB_HOST}:${CB_PORT}/statistics

echo "=================="
echo "Last day stability"
echo "=================="
YESTERDAY_M=$(date -d "yesterday" +"%b")
YESTERDAY_D=$(date -d "yesterday" +"%e")
/usr/local/bin/monit_log_processing.py /var/log/contextBroker/monitBROKER.log contextBroker $YESTERDAY_M $YESTERDAY_D

echo "============="
echo "Reset section"
echo "============="

echo "--database count before reset:"
databaseCount

echo "--removing expired subscriptions"
/usr/local/bin/garbage-collector.py csubs casubs > /dev/null
$SCRIPTS_DIR/mongo-remove-expired-subs.sh

echo "--cleaning CEP singleton entity"
$SCRIPTS_DIR/clear-cep-singleton.sh -- > /dev/null
echo "--reset issues"
$SCRIPTS_DIR/mongo-remove-all-issues.sh
echo "--create initial issues"
curl -X POST ${E2I_HOST}:${E2I_PORT}/new_issue/OUTSMART.NODE_3508/LowBatteryAlert/Warning
echo
curl -X POST ${E2I_HOST}:${E2I_PORT}/new_issue/OUTSMART.NODE_3501/BrokenLamp/Critical
echo

echo "--database count after reset:"
databaseCount

echo "==============="
echo "General section"
echo "==============="

echo "--disk occupancy"
df -h

echo "======================"
echo "Context Broker section"
echo "======================"

echo "--version test:"
curl -s ${CB_HOST}:${CB_PORT}/version

echo "--subscriptions detail (reference is csubs with 6 documents and casubs with 1)"
/usr/local/bin/garbage-collector.py csubs casubs

echo "--last times:"
cd $SCRIPTS_DIR && ./last-times.py

/usr/local/bin/lastest-updates.py entities orion 29

echo "==========="
echo "CEP section"
echo "==========="
sleep 5s

# This is a node not actually used (so real information comming from sensors will never disturb the test)
NODE=3503

PREV_R=$(cd $SCRIPTS_DIR && ./get-from-regulator.py electricPotential | awk -F ':' '{print $2}' | tr -d ' ')
echo "--setting warning level electricPotential (previous value was: $PREV_R)"
cd $SCRIPTS_DIR && ./set-regulator.sh electricPotential -2 > /dev/null 
sleep 2s
cd $SCRIPTS_DIR && ./get-cep-singleton.py

sleep 5s

PREV_C=$(cd $SCRIPTS_DIR && ./get-from-nodes.py batteryCharge | grep $NODE | awk -F : '{print $2'} | tr -d ' ')
echo "--setting critical level batteryCharge in node $NODE (previous value was: $PREV_C)"
cd $SCRIPTS_DIR && ./set-node.sh $NODE batteryCharge 2 > /dev/null
sleep 40s
cd $SCRIPTS_DIR && ./get-cep-singleton.py

echo "--issues list"
sleep 2s
cd $SCRIPTS_DIR && ./get-issues.py 

cd $SCRIPTS_DIR && ./set-regulator.sh electricPotential $PREV_R > /dev/null
cd $SCRIPTS_DIR && ./set-node.sh $NODE batteryCharge $PREV_C > /dev/null

echo "============"
echo "LOCS section"
echo "============"

cd $LDAPP_DIR/package/location2cb

echo "--stopping location2cb process"
PID=$(ps ax | grep location2cb | grep -v grep | awk '{print $1}')
echo "PID=$PID"
kill $PID
sleep 1s

# The stop/init cycle is disabled by default, given it could stress
# the simulation location tool
#echo "--stop vans"
#./stop_vans.py
#
#echo "--init vans"
#./init_vans.py
#sleep 3s

echo "--get simulation status"
$SCRIPTS_DIR/simulation-tool-status.sh

echo "--get vans"
./get_vans.py

echo "--starting location2cb again"
nohup ./location2cb.py > /dev/null 2> /dev/null &
sleep 4s
ps axf | grep location2cb | grep -v grep

echo "--check that some vans are moving after 4 seconds"
cd $SCRIPTS_DIR
echo -e "van1\tvan2\tvan3\tvan4"
printVans
sleep 4s
printVans
sleep 4s
printVans

# FI-WARE Live Demo Application

The FI-WARE Smart City Live Demo (aka "FI-WARE LiveDemo application") is a proof of concept that illustrates the usage of the FI-WARE  Generic Enablers to easily build rich applications for smart cities. The Smart City Live Demo is an application for the management of street lamps maintenance workforce in a city. The Smart City Live Demo is hosted and executed from the cloud capabilities of FI-Lab: all the GEs are deployed and run on FI-Lab virtual machines, and several of them are offered secured and "as a Service". It consists of a set of sensors deployed in Santander city center to gather electric parameters, presence and lightning measures from various street lamps and other devices. This information is gathered through IoT GEs and published in FI-Lab through the Context Broker GE. Based on the measures gathered from sensors, the Complex Event Processing analyzes the information and triggers issues (alarms) under certain circumstances (e.g. sustained low battery metrics).  Moreover, through the Location GE the position information of the technicians mobile phones is also gathered and published. The application allows an operator to watch the measures from the sensors on the city map, check the triggered issues and their severity, and assign technicians from the workforce (for instance, the idle technician closer to the street lamp). It also shows historic information gathered from the sensors and eventually, to send remote commands to the devices. On the other hand, a technician can update the information about an issue by taking and uploading a picture of the streetlamp to the cloud storage capabilities. 

This repository contains different pieces of code used in the FI-WARE LiveDemo application, opened to developers
worldwide under AGPL license so they can have a look on how applications are built using the FI-WARE platform. If you haven't ever seen the FI-WARE LiveDemo application running, we suggest you to have a look to this video: http://www.youtube.com/watch?v=Wh_zPsLUg-8

This repository contains the pieces of code developed by Telefónica I+D, other pieces (developed by
other partners in the project) are available in the following locations:

* historymod module. Developed by Universidad Politécnica de Madrid (UPM). https://github.com/wirecloud-fiware/historymod
* Wirecloud mashup. Developed by Universidad Politécnica de Madrid (UPM). https://github.com/wirecloud-fiware/live-demo-macs
* Complex Event Processing (CEP) Rules (developed by IBM): https://forge.fi-ware.eu/scmrepos/svn/fiware/trunk/FI-WARE/Data/CEP/rule-examples/

Familiarity with LiveDemo architecture in general is required in order to fully understand this
documentation. In addition, knowledge on the following FI-WARE GEis:

* Orion Context Broker
* CEP
* Cosmos
* LOCS
* Wirecloud
* Store

Eventually we will provide that information (or links to that information) in this page.

## LiveDemo architecture

View 1 (high-level functional view)

![LiveDemo app view 1](/doc/LiveDemoArch-view1.png)

View 2 (deployment view including conecton to FI-LAB ContextBroker and Cosmos):

![LiveDemo app view 2](/doc/LiveDemoArch-view2.png)

## Content

This repository contains the following Python modules in the packages/ directory:

* event2issue: a process to receive CEP generated events and register/update the corresponding Issues in Orion Context
Broker
* location2cb: tools to init the LOCS GEi, schedule van routes and regularly update that information in Orion
Context Broker
* ngsi2cosmos: a process that receives notification updates from Orion Context Broker and write them in the HDFS
Cosmos cluster. __Warning: since March 2014 this component is deprecated. Thus, you are highly encouraged to use its sucessor: Cygnus, available at https://github.com/telefonicaid/fiware-connectors/tree/develop/flume.__



The required modules to run the Python modules are specified in the requirements.txt file in the repository root.

In addition, this repository includes several scripts to automate management tasks related with LiveDemo
application. They are located in the scripts/ directory. The examples/ directory contains several
examples used to program LOCS simulations.

Finally, you can find in the repository root a script named ld-watchdog.sh that can be used to check that
the LiveDemo application environment is correctly set up.

More detailed information on the different pieces follow in the next sections.

### event2issue

This process listens to updates in the CEP singleton entity (sent by Orion Context Broker as NGSI10 notifyContext
requests to the callback URL), process the information published by CEP in that entity and generates (or updates)
the corresponding Issue back in Orion Context Broker (using NGSI10 updateContext request).

Run it with:

```
./event2issue.py
```

You can specify as arguments the listening port, the Orion Context Broker URL and the Store URL:

```
./event2issue.py 5000 http://localhost:1026 http://localhost:80
```

This process logs to event2issue.log and uses the accounting_token.json file to store the credentials used
to interact with Store. It exports the following REST operations (see details in the source code):

* POST /notify, callback that Orion Context Broker invokes whenever a new CEP event occurs
* POST /set_accounting, to set the accounting token
* POST /new_issue/[affected_entity_id]/[type]/[severity], to create a new Issue programmatically (as alternative
to CEP-generated Issues through Orion Context Broker), e.g. a third-party application interacting with LiveDemo
application backend.
* POST /set_counter/<n>, set the issue counter, so next Issue created will have Issue<n> name
* POST /set_correlation/<n>, set the correlation token (used in interactions with Store)

### location2cb

LiveDemo simulates 4 vans moving by the city. Several tools are included in this module, to deal with this
simulation.

* init_van.py, to init vans simulation in LOCS GEi
```
./init_vans.py
```

* get_vans.py, to print van locations
```
./get_vans.py [period (default = 5 seconds)] [times (default once) (0 = forever)]
#e.g.: ./get_vans.py 10 0
```

* stop_vans.py, to stop van simulation in LOCS GEi
```
./stop_vans.py
```

* move_van.py, to program LOCS with van movement from one point to another. Only van A and B are allowed to move this
way, from A1 to Ex (and back) for van A and from B1 to Ex (and back). Look to the points.csv file for the coordinates
associated to each point (they are in Santander city, but you could adapt this file to use yours). The default velocity
is 20 km/h (to change it you need to edit template.xml).
```
./move_van.py [van_msisdn] [from] [to]"
#e.g.: ./move_van.py 34621898316 A1 E7"
```

* location2cb.py, deals with Orion Context Broker interactions. This tool can be used in two ways. If arguments are
provided then it works without interacting with LOCS (this mode is thought when LOCS is not available or it is failing),
moving a van from one point to another (pretty much the same than move_van.py described above). If no arguments are
provided, then it just queries vans location from LOCS and updates the corresponding entities in Orion Context Broker.
```
# autonomous mode
./location2cb.py 34621898316 A1 E7"
# not autonomous mode
./location2cb.py
```

### ngsi2cosmos

__Warning: since March 2014 this component is deprecated. Thus, you are highly encouraged to use its sucessor: Cygnus, available at https://github.com/telefonicaid/fiware-connectors/tree/develop/flume.__

This process listens to NGSI10 notifyContext requests sent by Orion Context Broker to the callback URL, then appends
the values of each entity attribute to a file in the HDFS filesystem used by Cosmos (a different file is used for
each entity-attribute pair). The attribute value is timestamped with the current time. This way, historical
entity-attribute information can be used in Cosmos map-reduce jobs.

Run it with:

```
./ngsi2cosmos.py
```

You can specify as arguments the listening port and the Cosmos namenode URL:

```
./ngsi2cosmos.py 1028 http://localhost:14000
```

As additional optaional arguments you can specify directly the HDFS directory to use (default is base_dir), 
HDFS user (default is cosmos_user) and disable logging (using "log_off", otherwise logging is activated)

```
./ngsi2cosmos.py 1028 http://localhost:14000 /user/fermin fermin log_off
```

This process logs to ngsi2cosmos.log. It supports two HDFS backends: HttpFS and WebHDFS (the first one is preferred
and used by default, given that it doesn't need cluster complete exposure, only needs access to the namenode). It
exports only one REST operations (see details in the source code):

* POST /notify, callback that Orion Context Broker invokes whenever a new notifyContext request is sent

In addition, this package includes a helper script named list_status_pretty.py that can be used to print a status
report of the files in the HDFS backend. This script list files in the default HDFS directory (based_dir) but a
different one can be specified as script argument.

For mor information on how to connect Orion to Cosmos, check this link: https://forge.fi-ware.eu/plugins/mediawiki/wiki/fiware/index.php/How_to_persist_Orion_data_in_Cosmos

### management scripts

* iptables/, this directory contains scripts to turn on/off reporting from IDAS platform, manipulating iptables rules.
Disabling IDAS updates can be useful to debug, in order to avoid "noise" introduced by information coming from real
sensors during a testing session. Scripts in this directory require superuser privileges to run.

* bootstrapping/, this directory contains a not comprehensive set of scripts used to "bootstrap" the LiveDemo.
In particular:
    * 00_register_idas_entities/, contains scripts for creating Nodes, AMMS and Regulator in Orion Context Broker
    * 01_createCepEntity.sh, creates the CEP singleton entity (this entity is used by the event2issue.py process). This
      script is very similar to clear-cep-singleton.sh (using APPEND as action insted of UPDATE)
    * 02_subscribeEvent2Issue.sh, subscribes the event2issue callback for notifications
    * 03_subscribeCep.sh, subscribes CEP to changes in Nodes, AMMS and Regulator, so CEP is notified each time a
      change occurs in these entities (these changes in sequence can trigger rules which result are events published
      in the CEP singleton entity)
    * 04_setTechnicians.sh, creates and sets technicians information. It requires four arguments: the 
      phone numbers to use for the technicians.
    * 05_vansInit.sh, create the four van entities. It can be also used to reset vans to their initial positions
    * 06_subscribeCygnus.sh, subscribe the Cygnus callback for notifications
    * 07_subscribeFederatedCB-sensors.sh, subscribe a federated CB (orion2 in the file) to sensor notifications
    * 08_subscribeFederatedCB-vans.sh, subscribe a federated CB (orion2 in the file) to van notifications
    * 09_subscribeFederatedCB-issues.sh, subscribe a federated CB (orion2 in the file) to issue notifications

* get-from-amms.py: pretty-prints a given attribute for all AMMS (attribute name passed as argument). It
relies on query-amms.sh script, which encapsulates the actual NGSI request issued to Orion Context Broker.
```
./get-from-amms.py ActivePower
```

* get-from-nodes.py: pretty-prints a given attribute for all Nodes (attribute name passed as argument). It
relies on query-node.sh script, which encapsulates the actual NGSI request issued to Orion Context Broker.
```
./get-from-node.py batteryCharge
```

* get-from-regulator.py: pretty-prints a given attribute for the Regulator (attribute name passed as argument).
It relies on query-regulator.sh script, which encapsulates the actual NGSI request issued to Orion Context Broker.
```
./get-from-regulator.py ActivePower
```

* get-issues.py: pretty-prints a list with all issues. It relies on query-issue.sh script, which encapsulates
the actual NGSI request issued to Orion Context Broker.

* get-technician.py: pretty-prints a list with all technicians. It relies on query-technician.sh script, which
encapsulates the actual NGSI request issued to Orion Context Broker.

* get-van.py: pretty-prints a list wih all vans. It relies on query-van.sh script, which
encapsulates the actual NGSI request issued to Orion Context Broker.

* last-times.py: prints the last time Nodes, AMMS and Regulator were modified. It relies on query-all.sh script, which
encapsulates the actual NGSI request issued to Orion Context Broker.

* set-amms.sh: set a given attribute of a given AMMS with a given value, passed as argument.
```
./set-amms.sh 06E1E5B2100394784 electricalPotential -2
```

* set-node.sh: set a given attribute of a given Node with a given value, passed as argument.
```
./set-node.sh 3501 batteryCharge
```

* erase-node-date.sh: erases the TimeInstant of a given Node, setting it to "None"
```
./erase-node-date.sh 3512
```

* set-regulator.sh: set a given attribute of the Regulator with a given value, passed as argument.
```
./set-regulator.sh electricalPotential -7
```

* close-issue.sh: set closingDate attribute to current time on a given Issue (which number is passed as argument),
which means "closing the issue" according to LiveDemo application semantics.
```
./close-issue.sh 23
```

* get-cep-singleton.py: pretty-prints the attributes of the CEP singleton entity. It relies on query-cep-singleton.sh
script, which encapsulates the actual NGSI request issued to Orion Context Broker.

* cep-start.sh, cep-stop.sh, cep-status.sh: use them to start/stop CEP or report its status

* clear-cep-singleton.sh: clears the CEP singleton entity, setting all its attributes with the value passed as argument.
```
./clear-cep-singleton.sh foo
```

* mongo-remove-all-issues.sh: removes all issues in MongoDB

* mongo-remove-expired-subs.sh: removes all expired subscriptions in MongoDB (after running the garbage-collector.py
program tha comes with Orion Context Broker RPM).

* mongo-remove-id.sh: removes a given registration/entity associated in MongoDB, identified by its ID.
```
./mongo-remove-id.sh Issue27
```

* new-cep-event.sh: emulates a CEP event directly updating the CEP singleton entity (instead of using CEP). This script
takes the following parameters: entity ID, entity type, event type and severity. Only for debugging purposes.

* register-issue.sh: emulates a direct Issue registration (instead of using event2issue). Only for debugging purposes.

* renew-cb-log.sh: rotate Orion Context Broker log. This script has not been testbed so much, so it may fail.

* simulation-tool-restart.sh: wrapper of the REST operation to start/restart the simulation tool (part of LOCS).

* simulation-tool-status.sh: wrapper of the REST operation to get the status of the simulation tool.

* event2issue-test/, this directory contains some scripts to test event2issue process. Not too interesting, by the way.

## Putting all together: typical sequence of commands running LiveDemo app ##

This section shows a sequence of commands corresponding to a typical test execution of LiveDemo application, for
illustration purposes.

```
# First of all, run the needed scripts in bootstrapping/ directory

# remove all issues due to start
./mongo-remove-all-issues.sh

# stop IDAS reporting
sudo iptables/turn_off_idas.sh

# init vans
python init_vans.py

# create some initial issues
curl -X POST localhost:5000/new_issue/OUTSMART.NODE_3508/LowBatteryAlert/Warning
curl -X POST localhost:5000/new_issue/OUTSMART.NODE_3501/BrokenLamp/Critical

# create issue with mobile on 3500

# create an issue in Regulator due to problems with electricPotential
# (commented lines is the alternative way in the case CEP generated issues are not working)
./get-from-regulator.py electricPotential  # to know the previous level
./set-regulator.sh electricPotential -2
#curl -X POST localhost:5000/new_issue/OUTSMART.RG_LAS_LLAMAS_01/LowElectricPotential/Warning
./set-regulator.sh electricPotential -7
#curl -X POST localhost:5000/new_issue/OUTSMART.RG_LAS_LLAMAS_01/LowElectricPotential/Critical

# create an issue in Node due to problems with batteryCharge
# (commented lines is the alternative way in the case CEP generated issues are not working)
./get-from-nodes.py batteryCharge # to know the previous level
./set-node.sh 3506 batteryCharge 10 ; date
#curl -X POST localhost:5000/new_issue/OUTSMART.NODE_3506/LowBatteryAlert/Warning
./set-node.sh 3506 batteryCharge 3 ; date
#curl -X POST localhost:5000/new_issue/OUTSMART.NODE_3506/LowBatteryAlert/Critical

# At this moment we have the following issues on the map:
# 3508
# 3501
# 3500
# Regulator
# 3506

#move Marcos to repair 3501
python move_van.py 34604872235 B1 E7
#python location2cb.py 34604872235 B1 E7  # in the case LOCS is not working

#move Marcos back to home
python move_van.py 34604872235 E7 B1
#python location2cb.py 34604872235 E7 B1  # in the case LOCS is not working

#move Jacinto to repair 3506
python move_van.py 34669079467 A1 E1
#python location2cb.py 34669079467 A1 E1  # in the case LOCS is not working

#move Jacinto back to home
python move_van.py 34669079467 E1 A1
#python location2cb.py 34669079467 E1 A1  # in the case LOCS is not working

#restore values previous to manipulation
./set-regulator.sh electricPotential <prev_level>
./set-node.sh 3506 batteryCharge <prev_level>

#turn on IDAS again
sudo iptables/turn_on_idas.sh

#stop vans
python stop_vans.py
```

## Security consideration

Due to security reasons, all the URLs in code, configuration and this documentation itself are not using actual IPs
or DNS names. All are set to localhost. Of course, replace it with the right ones (in the FI-WARE GEi global or
dedicated instances you were using) before running the software.

To ease the task, all the parameters you need to configure for shell scripts (.sh files) are in the scripts/ENV.sh 
file. Just edit that file and load it in your environment using:

```
. ENV.sh
```

Parameters:

* CEP_HOST and CEP_PORT where the CEP runs
* CB_HOST and CB_PORT where the Orion Context Broker runs
* FED_CB_HOST and FED_CB_PORT where the federated Orion Context Broker runs
* E2I_HOST and E2I_PORT where the event2issue runs
* CYGNUS_HOST and CYGNUS_PORT where Cygnus runs
* IDAS_HOST where IDAS runs

In addition, for Python code, you need to modify env.py files in the following places:

* In package/event2issue/env.py, set cb_url and store_url to the actual URLs
* In package/location2cb/env.py, set locs_host to the LOCS actual host IP/name
* In package/ngsi2cosmos/env.py, set cosmos_url properly to the URL where COSMOS HttpFs is listening, cosmos_user to the proper HDFS user and base_dir to the proper directory within the HDFS directory. __Warning: since March 2014 this component is deprecated. Thus, you are highly encouraged to use its sucessor: Cygnus, available at https://github.com/telefonicaid/fiware-connectors/tree/develop/flume.__

## Contact

For any question, bug report, suggestion or feedback in general, please contact with Fermín Galán (fermin at tid dot es).
If I don't know the answer I will redirect you to the right contact :)

## License

This code is licensed under GNU Affero General Public License v3. You can find the license text in the LICENSE file
in the repository root.

# Cosmos Demo Applications
Cosmos is the reference implementation of the Big Data GE, and its FI-LAB Global Instance (also called in this document Cosmos cluster, or cluster) holds several public datasets regarding certain spanish Smart Cities.

Some applications exploiting those datasets have been developed for demostration purposes, and they are documented in the next sections.

## Plague Tracker
Conceptually speaking, this is an application running on top of the Cosmos Global Instance in FI-LAB. The Plague Tracker accesses and processes the historical data about the plagues affecting the spanish city of Malaga. More details on the nature, representation formats, location, etc. of the data can be found at:

http://forge.fi-ware.eu/plugins/mediawiki/wiki/fiware/index.php/M%C3%A1laga_open_datasets#Plagues_tracking

Under the above concept there is a Java-based Hive client querying the Cosmos cluster through the TCP/10000 port, where a Hive server listens for incoming connections. This Hive client is governed by a Web application exposing a GUI (a map of the city of Malaga and a set of controls) the final user operates in order to get certain visualizations of the data. These visualizations/operations are:
- Get the current focuses. The map shows the neighbourhoods affected by the selected type of plague. A neighbourhood is affected by a plague if a technician had to work in mitigating the plague in that neighbourhood the last month.
- Get an infection forecast. The map shows a forecast about the neighbourhoods that will probably fe infected by the selected type of plague. The forecast is based on the historical number of incidences, the weather and the proximity to already infected neighbourhoods.

The plague types the user can select are:
- Rats
- Mice
- Pigeons
- Cockroaches
- Bees
- Wasps
- Ticks
- Fleas

In addition to the map, three charts show the correlation index between the selected type of plague and three ambiental parameters such as the temperature, the rainfall and the humidity. These ambiental parameters are got from another dataset related to the city of Malaga:

http://forge.fi-ware.eu/plugins/mediawiki/wiki/fiware/index.php/M%C3%A1laga_open_datasets#Weather

### Requirements, dependencies and security concerns
Being a web application, the Plague Tracker needs an applications server such as Tomcat. The current code has been tested on Tomcat 7.0.14.0.

The code depends on Hive (0.7.1 or higher), Hadoop (0.20 / CDH3) and Gson (0.7.1 or higher). Nevertheless, the dependencies are automatically managed by Maven (see the pom.xml file), thus nothing should be done regarding this.

If you are thinking on deploying your own instance of the application, please take into account the hosting server will need permissions for accessing the Cosmos Global Instance. This is not a constraing when the hosting server is a virtual machine from FI-WARE, created through the FI-LAB Portal (http://lab.fi-lab.eu).

### Already deployed instances of this application
http://130.206.81.65:8080/plague-tracker/

## Contact
For any question, bug report, suggestion or feedback in general, please contact with Francisco Romero (frb at tid dot es).

## License
This code is licensed under GNU Affero General Public License v3. You can find the license text in the LICENSE file in the repository root.

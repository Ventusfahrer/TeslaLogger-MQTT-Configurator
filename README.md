# TeslaLogger-MQTT-Configurator
a very basic prototype script to define TeslaLogger MQTT-data to HomeAssistant

This is a prototype to bring MQTT-Data of the Teslalogger to HomeAssistant using HomeAssistant's MQTT Auto Discovery. This avoids the need to define entity by entity in the configuration.yaml in order to get HA access to it.

## The Prototype is based on following configuration:

- MQTT-AddOn is installed and configured in HomeAssistant
  - using username password as authentification mechanism is possible
- TeslaLoggers 1.55 installed and running
- MQTTClient.exe is configured via MQTTClient.exe.config to the HomeAssistant MQTT-Broker
  - the value of the MQTT-Setting for **Topic** is the car's name
  - changes are forwarded to MQTT. This check can be done using [mqtt_explorer](https://mqtt-explorer.com/)
- pyhton3 needs to be installed
- pyhton-paho-mqtt needs to be installed
## Prepapration

* Download tlHAautoDiscover.py and edit the script

* Adapt following variables to your configuration:

```
CarName = '\exactly the same name as the TOPIC value in mqtt config>'
VIN  = '<the VIN of the car or a at least 5 character long string>'
MQTT_USER = 'to be changed'
MQTT_PASSWORD = 'to be changed'
MQTT_HOST = 'home assistant host name'
MQTT_PORT = 1883 #default port of the HA MQTT-Broker
```
## Execute the Script

```
python3 tlHAautoDiscovery.py
```

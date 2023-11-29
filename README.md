# TeslaLogger-MQTT-Configurator
a very basic prototype script to define TeslaLogger MQTT-data to HomeAssistant

This is a prototype to bring MQTT-Data of the Teslalogger to HomeAssistant using HomeAssistant's MQTT Auto Discovery. This avoids the need to define entity by entity in the configuration.yaml in order to get HA access to it.

The Prototype is based on following configuration:

- MQTT-AddOn is installed an configured in HomeAssistant
  - using username password as authentification mechanism
- TeslaLoggers 1.55 installed and running
  - MQTTClient.exe is configured via MQTTClient.exe.config to write MQTT to HomeAssistant MQTT-Broker
  - the value of the MQTT-Setting for **Topic** is the car's name
- 

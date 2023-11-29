#!/usr/bin/python3

import paho.mqtt.client as mqtt
import json
import time


CarName = '<change me>'
VIN=''  # standard length 17 characters A-Z,0-9
#    01234567890123456

MQTT_USER = '<change me>'
MQTT_PASSWORD = '<change me>'
MQTT_HOST = '<change me>'
MQTT_PORT = 1883  # check me

clPresent=0
clClass=1
clUoM=2

devClassArr = {
    "charging": [False, None, None],
    "driving": [False, None, None],
    "online": [False, None, None],
    "sleeping": [False, None, None],
    "falling_asleep": [False, None, None], 
    "speed": [False, "speed", "km/h"],         
    "power": [False, "power", "kW"],
    "odometer": [False, "distance", "km"],
    "ideal_battery_range_km": [False, "distance", "km"],
    "battery_range_km": [False, "distance", "km"],
    "outside_temp": [False, "temperature", "°C"],
    "battery_level": [False, "battery", "%"],
    "charger_voltage": [False, "voltage", "V"], 
    "charger_phases": [False, None, None],
    "charger_actual_current": [False, "current", "A"],
    "charge_energy_added": [False, "energy", "kWh"],
    "charger_power": [False, "power", "kW"],
    "charge_rate_km": [False, "distance", "km"],
    "charge_port_door_open": [False, None, None],
    "time_to_full_charge": [False, "duration", None],
    "fast_charger_present": [False, None, None],
    "trip_start": [False, None, None],
    "trip_start_dt": [False, "timestamp", None],
    "trip_max_speed": [False, "speed", "km/h"],
    "trip_max_power": [False, "power", "kW"],
    "trip_duration_sec": [False, "duration", "s"],
    "trip_kwh": [False, "energy", "kWh"], 
    "trip_avg_kwh": [False, "energy", "kWh"],
    "trip_distance": [False, "distance", "km"],
    "ts": [False, "timestamp", None],
    "latitude": [False, None, None],
    "longitude": [False, None, None],
    "charge_limit_soc": [False, None, "%"],
    "inside_temperature": [False, "temperature", "°C"],
    "battery_heater": [False, None, None],
    "is_preconditioning": [False, None, None],
    "sentry_mode": [False, None, None],
    "display_name": [False, None, None],
    "heading": [False, None, None],

 #   the following sensors are commented because they
 #   often have NULL values, which is causing frequently
 #   error messages in HA Protocolfile
 #   "active_route_destination": [False, None, None],
 #   "active_route_energy_at_arrival": [False, "energy", "kWh"],
 #   "active_route_minutes_to_arrival": [False, "duration", "min"],
 #   "active_route_traffic_minutes_delay": [False, "duration", "min"],
 #   "active_route_latitude": [False, None, None],
 #   "active_route_longitude": [False, None, None],
    
    "open_windows": [False, None, None],
    "open_doors": [False, None, None],
    "frunk": [False, None, None],
    "trunk": [False, None, None],
    "locked": [False, None, None],
    "TLGeofencea": [False, None, None],
    "TLGeofenceIsHome": [False, None, None],
    "TLGeofenceIsCharger": [False, None, None],
    "TLGeofenceIsWork": [False, None, None],
    "open_windows": [False, None, None],
    "open_doors": [False, None, None],
    "frunk": [False, None, None],
    "trunk": [False, None, None],
    "locked": [False, None, None],
    "TLGeofencea": [False, None, None],
    "TLGeofenceIsHome": [False, None, None],
    "TLGeofenceIsCharger": [False, None, None],
    "TLGeofenceIsWork": [False, None, None],
    "car_version": [False, None, None],
    "country_code": [False, None, None],
    "state": [False, None, None],
    "software_update_version": [False, None, None]
}

sensorArr={}
vinlen = len(VIN)

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

def on_message(mqttc, obj, msg):
    # print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    sensorArr[msg.topic[len(CarName)+1:]] = 1
    print(msg.topic[len(CarName)+1:])

def on_publish(mqttc, obj, mid):
    # print("mid: " + str(mid))
    pass

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log


CarID = VIN[vinlen-6:vinlen-1]

mqttc.username_pw_set(MQTT_USER, MQTT_PASSWORD)
mqttc.connect(MQTT_HOST, MQTT_PORT, 20)
mqttc.subscribe(f'{CarName}/#', 0)

mqttc.loop_start()
time.sleep(5)

mqtt_device = {  
          "identifiers":[ f'{CarName}_{CarID}' ], 
          "name": f'{CarName}',
          "mf": 'TeslaLogger',
          "mdl": "MQTT_Export"          
        }

def topicAndMessage(sensorName):
    
    sDict={}
    
    try:
        devClass = devClassArr[sensorName][clClass]
    except KeyError as e:
        return None, None
    finally:
        pass

    unitOfMeas = devClassArr[sensorName][clUoM]

    sDict["name"] = sensorName
    if not devClass == None:
        sDict["device_class"] = devClass
    if not unitOfMeas == None:
        sDict["unit_of_meas"] = unitOfMeas
    sDict["state_topic"] = f'{CarName}/{sensorName}'
    sDict["unique_id"] = f'{CarID}_{sensorName}'
    sDict["device"] = mqtt_device
 
    message =json.dumps(sDict)
    topic = f'homeassistant/sensor/{CarName}/{sensorName}/config'

    return topic, message

for sensor in sensorArr:

    topic, message = topicAndMessage(sensor)

    if not topic == None and not message == None:
        mqttc.publish(topic, message, qos=1, retain=True)
        devClassArr[sensor][clPresent] = True
        print(topic)
        print(f'  {message}')
        mqttc.loop_write()


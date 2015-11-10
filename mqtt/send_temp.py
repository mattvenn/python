#!/usr/bin/python
import paho.mqtt.client as mqtt
import time
import sys
import requests
import json
import os

#public_key = '7JD1NG3mWNuGVqEpqWK0'  # dust
public_key = 'J9bKz84Wx8CX4ryLvAJYuv9o3NP'  # valencia temp

def fetch_temp():
    url = 'http://phant.cursivedata.co.uk/output/' + public_key + '.json'
    payload = {'gte[timestamp]': 'now-5minutes'}
    r = requests.get(url, params=payload)
    return float(json.loads(r.text)[0]['temp'])

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_publish(client, userdata, mid):
    print("sent to client")
    print client
    print userdata
    print mid


temp = fetch_temp()
if temp is None:
    print("problem fetching data")
    exit(0)
else:
    temp = int(temp * 250)
    print("sending temp=%d" % temp)
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish

client.connect("192.168.0.200", 1883, 60)
time.sleep(0.1)
client.loop_start()

stat, mid = client.publish("/dial/guage", temp, qos=2)
if stat != mqtt.MQTT_ERR_SUCCESS:
    print("problem sending")
else:
    print("message sent id %d" % mid)

client.loop_stop()
client.disconnect()

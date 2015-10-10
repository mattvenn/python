#!/usr/bin/python
import paho.mqtt.client as mqtt
import time
import sys
import requests
from secrets import public_key
import json
import os

def fetch_dust():
    url = 'https://data.sparkfun.com/output/' + public_key + '.json'
    payload = {'gte[timestamp]': 'now-5minutes'}
    #r = requests.get(url, params=payload)  # not working
    status = os.system('wget https://data.sparkfun.com/output/7JD1NG3mWNuGVqEpqWK0.json?gte[timestamp]=now%20-5minutes -O out.json -o wget.log')
    if status == 0:
        with open('out.json') as fh:
            js = json.load(fh)
            return float(js[0]['dust'])

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_publish(client, userdata, mid):
    print("sent to client")
    print client
    print userdata
    print mid


dust = fetch_dust()
if dust is None:
    print("problem fetching data")
    exit(0)
else:
    dust = int(dust / 3)
    print("sending dust=%d" % dust)
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish

client.connect("192.168.0.200", 1883, 60)
time.sleep(0.1)
client.loop_start()

stat, mid = client.publish("/dial/guage", dust, qos=2)
if stat != mqtt.MQTT_ERR_SUCCESS:
    print("problem sending")
else:
    print("message sent id %d" % mid)

client.loop_stop()
client.disconnect()

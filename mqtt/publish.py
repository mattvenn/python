#!/usr/bin/python
import paho.mqtt.client as mqtt
import time
import sys

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_publish(client, userdata, mid):
    print("sent to client")
    print client
    print userdata
    print mid

client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish

client.connect("192.168.0.200", 1883, 60)
time.sleep(0.1)
client.loop_start()

#just show the date
import datetime
minute = datetime.datetime.now().minute
out = int((minute / 60.0 ) * 1000)
print(out)
stat, mid = client.publish("/dial/guage", out, qos=2)
if stat != mqtt.MQTT_ERR_SUCCESS:
    print("problem sending")
else:
    print("message sent id %d" % mid)
"""
min = 20
max = 1010
step = (max-min)/10
for t in range(min,max+step,step):
    print t
    r = client.publish("/dial/guage", t)
    time.sleep(1)
"""
time.sleep(2)
client.loop_stop()
client.disconnect()

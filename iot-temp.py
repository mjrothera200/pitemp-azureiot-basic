#!/usr/bin/python3
import paho.mqtt.client as paho
import json
import RPi.GPIO as GPIO
import dht11
from time import sleep
from time import time
import datetime
import ssl
from base64 import b64encode, b64decode
from hashlib import sha256
from time import time
from urllib import parse
from hmac import HMAC


def generate_sas_token(uri, key, policy_name=None, expiry=3600):
        ttl = time() + expiry
        sign_key = "%s\n%d" % ((parse.quote_plus(uri)), int(ttl))
        print(sign_key)
        signature = b64encode(HMAC(b64decode(key), sign_key.encode('utf-8'), sha256).digest())
        rawtoken = {
                'sr' :  uri,
                'sig': signature,
                'se' : str(int(ttl))
                }
        if policy_name is not None:
                rawtoken['skn'] = policy_name

        return 'SharedAccessSignature ' + parse.urlencode(rawtoken)



# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# read data using pin 17
instance = dht11.DHT11(pin=17)

# device credentials
ca_absolute_path = '/home/pi/dev/iot-temp/pitemp-azureiot-basic/baltimorebase64.cer'
iothubname = 'mjrothera200'
deviceid = 'pi1'  # Azure IoT Device ID
username = 'mjrothera200.azure-devices.net/pi1'
primarykey = 'F1ewFxFWM/PytVHeGCrE2AV/6j7vlhv1QZuK8qplo5Q='

sas_token = generate_sas_token(iothubname+'.azure-devices.net/devices/'+deviceid, primarykey)
print(sas_token)

# extract the serial number
cpuserial = "0000000000000000"
try:
    f=open('/proc/cpuinfo', 'r')
    for line in f:
        if line[0:6]=='Serial':
            cpuserial = line[10:26]
    f.close()
except:
    cpuserial="ERROR000000000"

print("CPU Serial # is %s" % (cpuserial))


# device topics
out_topic_environmentals = 'devices/' + deviceid + '/messages/events/'  # publishing messages


# --------------- #
# Callback events #
# --------------- #

# connection event
def on_connect(client, data, flags, rc):
    print('Connected, rc: ' + str(rc))

# connection event

def on_disconnect(client, data, rc):
    print('Disonnected, rc: ' + str(rc))

# subscription event
def on_subscribe(client, userdata, mid, gqos):
    print('Subscribed: ' + str(mid))

# received message event
def on_message(client, obj, msg):
    print(msg.topic)
# ------------- #
# MQTT settings #
# ------------- #

# create the MQTT client
client = paho.Client(client_id=deviceid, protocol=paho.MQTTv311)  # * set a random string (max 23 chars)

# assign event callbacks
client.on_message = on_message
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe


# client connection
client.username_pw_set(username, sas_token)  # MQTT server credentials
client.tls_set(ca_certs=ca_absolute_path, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)

try:
    client.connect(iothubname+".azure-devices.net", port=8883)                   # MQTT server address
    client.subscribe(in_topic_snapshot, 0)                     # MQTT subscribtion (with QoS level 0)
except:
    print('could not connect')
    

client.loop_start()

while True:
	sleep( 6 )
	result = instance.read()
	if result.is_valid():
		temp_c = result.temperature 
		temp_f = (result.temperature * 9)/5 + 32 
		humidity = result.humidity 
		message = { 'temp_c': temp_c, 'temp_f': temp_f, 'humidity': humidity }     
		client.publish(out_topic_environmentals, json.dumps(message))






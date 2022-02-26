#from influxdb_client import InfluxDBClient, Point
#from influxdb_client.client.write_api import SYNCHRONOUS
#from time import gmtime, strftime
import time
import paho.mqtt.client as mqtt
#import requests
import sys


argState = sys.argv[1]
#push to cmnd/Fuellstand/POWER ON/OFF
TOPIC = "cmnd/Fuellstand/POWER"

BROKER_ADDRESS = "127.0.0.1"

PORT = 1881

QOS = 1


#def on_publish():
#    print("data published \n")

#def on_connect(client, userdata, flags, rc):
#    print("connected")

#def on_subscribe(client, userdata, mid, granted_qos):
#    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
#    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    print("message ", str(msg.payload.decode("utf-8")))




mqttclient = mqtt.Client()

mqttclient.username_pw_set("python", "h56u7ijSDFRT6")



#mqttclient.on_subscribe = on_subscribe
mqttclient.on_message = on_message
#mqttclient.on_connect = on_connect
#mqttclient.on_publish = on_publish
#mqttclient.subscribe(TOPIC, qos=QOS)




mqttclient.connect(BROKER_ADDRESS, PORT)

#time = strftime("%Y-%m-%dT%H:%M:%S", gmtime())


mqttclient.loop_start()

mqttclient.subscribe("cmnd/Fuellstand/POWER")


DATA = str(argState) #"{\"Time\":\"" + str(time) + "\",power "+ str(data) + "}"

mqttclient.publish(TOPIC, DATA, qos = QOS)


time.sleep(4)

mqttclient.loop_stop()

#print(str(a.is_published()))


#print(type(a[0]))

#b = str(a.is_published)

#print(str(a[0]))

##############
#
#   Skript mit Parametern ausführen: "pumpeMqtt.py on" bzw. "pumpeMqtt.py off"
#
##############

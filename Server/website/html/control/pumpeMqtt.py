#from influxdb_client import InfluxDBClient, Point
#from influxdb_client.client.write_api import SYNCHRONOUS
#from time import gmtime, strftime
#import time
import paho.mqtt.client as mqtt
#import requests
import sys


argState = sys.argv[1]
#push to cmnd/Fuellstand/POWER ON/OFF
TOPIC = "cmnd/Fuellstand/POWER"

BROKER_ADDRESS = "mosquitto"

PORT = 1881

QOS = 1

mqttclient = mqtt.Client()

mqttclient.username_pw_set("python", "h56u7ijSDFRT6")

mqttclient.connect(BROKER_ADDRESS, PORT)

#time = strftime("%Y-%m-%dT%H:%M:%S", gmtime())

DATA = str(argState) #"{\"Time\":\"" + str(time) + "\",power "+ str(data) + "}"

mqttclient.publish(TOPIC, DATA, qos = QOS)

##############
#
#   Skript mit Parametern ausfuehren: "pumpeMqtt.py on" bzw. "pumpe.py off"
#
##############

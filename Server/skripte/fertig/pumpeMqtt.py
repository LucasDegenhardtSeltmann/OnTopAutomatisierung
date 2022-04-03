import paho.mqtt.client as mqtt
import sys

argState = sys.argv[1]

TOPIC = "cmnd/Fuellstand/POWER"

BROKER_ADDRESS = "mosquitto"

PORT = 1881

QOS = 1

mqttclient = mqtt.Client()

mqttclient.username_pw_set("python", "h56u7ijSDFRT6")

mqttclient.connect(BROKER_ADDRESS, PORT)

DATA = str(argState)

mqttclient.publish(TOPIC, DATA, qos = QOS)

##############
#
#   Skript mit Parametern ausführen: "pumpeMqtt.py on" bzw. "pumpeMqtt.py off"
#
##############

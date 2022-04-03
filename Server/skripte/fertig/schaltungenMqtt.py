from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import time
import paho.mqtt.client as mqtt


def influxInit():
    global influxclient
    influxclient = InfluxDBClient(url = "http://localhost:8086", token = "influxdbtoken", org = "ontop.hs-bochum.de")

    global write_api
    global query_api
    write_api = influxclient.write_api(write_options = SYNCHRONOUS)
    query_api = influxclient.query_api()


def nodesInit():
    global nodes
    nodes = []
    global pumpe

    #nodes.append(["ip", "MQTT-Topic", "ON"])#Beschreibung
    nodes.append(["10.5.35.54", "Erdbeet", "OFF"])#Erdbeet 1

    pumpe = ["10.5.33.64", "Fuellstand", "OFF"]#Pumpe

    mqttWrite()
    time.sleep(10)

    for node in nodes:
        mqttWrite("cmnd", node[1], "POWER", "OFF")


def influxRead(topic):
    query = """ from (bucket:"initial")\
    |> range(start: -5m)\
    |> filter(fn:(r) => r[\"topic\"] == \"tele/"""+str(topic)+"""/SENSOR\")"""

    result = influxclient.query_api().query(query = query)

    results = []

    for table in result:
        for record in table.records:
            results.append((record.get_value(), record.get_field()))

    return results


def mqttWrite(topiclv1 = "cmnd", topiclv2 = "Fuellstand", topiclv3 = "POWER", data = "OFF"): #default stellt die Pumpe auf OFF
    TOPIC = str(topiclv1) + "/" + str(topiclv2) + "/" + str(topiclv3)

    BROKER_ADDRESS = "mosquitto"

    PORT = 1881

    QOS = 1

    mqttclient = mqtt.Client()

    mqttclient.username_pw_set("python", "h56u7ijSDFRT6")

    mqttclient.connect(BROKER_ADDRESS, PORT)

    DATA = data

    mqttclient.publish(TOPIC, DATA, qos = QOS)


def check(element):
    nodeCheck = influxRead(element[1]) #auslesen der aktuellen Bodenfeuchte

    try:
        bodenfeuchte = nodeCheck[0][0]
    except:
        bodenfeuchte = 999

    if(int(bodenfeuchte) <= 100 && element[2] == "OFF"):
        mqttWrite("cmnd", element[1], "POWER", "ON")
        element[2] = "ON"
        mqttWrite(data = "ON")
        pumpe[2] = "ON"

    elif(bodenfeuchte >= 300 && element[2] == "ON"):
        ventileAn = false
        for node in nodes:
            if not(node == element):
                if (node[2] == "ON"):
                    ventileAn = true

        if(ventileAus): #Wenn alle anderen Ventile OFF sind, setze die Pumpe auf OFF
            mqttWrite()
            pumpe[2] = "OFF"
            time.sleep(10)

        mqttWrite("cmnd", element[1], "POWER", "OFF")
        element[2] = "OFF"


def main():
    influxInit()
    
    nodesInit()

    while(1):
    
        for element in nodes:
            check(element)

        time.sleep(300)


if __name__ == "__main__":
    main()

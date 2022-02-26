from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from time import gmtime, strftime
import time
import paho.mqtt.client as mqtt


def influxInit():
    global influxclient
    influxclient = InfluxDBClient(url = "http://localhost:8086", token = "influxdbtoken", org = "ontop.hs-bochum.de")

    global write_api
    global query_api
    write_api = influxclient.write_api(write_options = SYNCHRONOUS)
    query_api = influxclient.query_api()


def influxRead(topic):
    query = """ from (bucket:"initial")\
    |> range(start: -5m)\
    |> filter(fn:(r) => r[\"topic\"] == \"tele/"""+str(topic)+"""/SENSOR\")"""

    result = influxclient.query_api().query(query = query)

    results = []

    for table in result:
        for record in table.records:
            results.append((record.get_value(), record.get_field()))

#    return results[0][0]

    return results


def influxWrite(topiclv1 = "tele", topiclv2 = "Fuellstand", topiclv3 = "RELAISE", data = "OFF"):
    time = strftime("%Y-%m-%dT%H:%M:%S", gmtime())

    DATA = "{\"Time\":\"" + str(time) + "\",\"Fuellstand\":" + str(data) + "}"

    mqttWrite(topiclv1, topiclv2, topiclv3, DATA)


def mqttWrite(topiclv1 = "cmnd", topiclv2 = "Fuellstand", topiclv3 = "RELAISE", data = "OFF"): #default stellt die Pumpe auf ON
    TOPIC = str(topiclv1) + "/" + str(topiclv2) + "/" + str(topiclv3)

    BROKER_ADDRESS = "127.0.0.1"

    PORT = 1881

    QOS = 1

    mqttclient = mqtt.Client()

    mqttclient.username_pw_set("python", "h56u7ijSDFRT6")

    mqttclient.connect(BROKER_ADDRESS, PORT)

#    time = strftime("%Y-%m-%dT%H:%M:%S", gmtime())

#    DATA = "{\"Time\":\"" + str(time) + "\","+ str(data) + "}"   #\"Liter\":" + str(liter) + "}"

    DATA = data

    mqttclient.publish(TOPIC, DATA, qos = QOS)


if __name__ == "__main__":

    influxInit()
    
    influxWrite()

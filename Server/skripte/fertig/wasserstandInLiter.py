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

def influxRead():
    query = """ from (bucket:"initial")\
    |> range(start: -5m)\
    |> filter(fn:(r) => r[\"topic\"] == \"tele/Fuellstand/SENSOR\")"""

    result = influxclient.query_api().query(query = query)

    results = []

    for table in result:
        for record in table.records:
            results.append((record.get_value(), record.get_field()))

    global abstand
    abstand = results[0][0]

def toLiter():
    global liter

    liter = (4320 * (1 - (abstand / 100) / 1.2))

    #1440 Liter bei 1,2L 1B 1,2H
    #*3 = 4320

def mqttWrite():
    TOPIC = "tele/Fuellstand/LITER"

    BROKER_ADDRESS = "127.0.0.1"

    PORT = 1881

    QOS = 1

    mqttclient = mqtt.Client()

    mqttclient.username_pw_set("python", "h56u7ijSDFRT6")

    mqttclient.connect(BROKER_ADDRESS, PORT)

    time = strftime("%Y-%m-%dT%H:%M:%S", gmtime())

    DATA = "{\"Time\":\"" + str(time) + "\",\"Liter\":" + str(liter) + "}"

    mqttclient.publish(TOPIC, DATA, qos = QOS)

if __name__ == "__main__":

    influxInit()

    while(1):

        influxRead()

        toLiter()

        mqttWrite()

        time.sleep(300)

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


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
    |> filter(fn:(r) => r[\"topic\"] == \"tele/Erdbeet/STATE\")"""

    query = """ from (bucket:"initial")\
    |> range(start: -10m)\
    |> filter(fn:(r) => r[\"topic\"] == \"tele/Fuellstand/SENSOR\")"""

    result = influxclient.query_api().query(query = query)

    results = []

    for table in result:
        for record in table.records:
            results.append((record.get_value(), record.get_field()))

    global abstand
    try:
        abstand = results[0][0]
    except:
        abstand = "nope"

    print("Res: " + str(results))



if __name__ == "__main__":

    influxInit()

    influxRead()

    print(str(abstand))

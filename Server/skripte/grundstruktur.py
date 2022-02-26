##################
#
#   Dieses Skript dient ausschliesslich als Grundstruktur zum automatisierten lesen
#   und schreiben in die InfluxDB, bzw. Senden von Befehlen an die Nodes fuer das
#   Projekt OnTop an der Hochschule Bochum. Zum bearbeiten sollte hiervon zunaechst
#   eine neue Kopie erstellt werden, anschließend koennen in der Kopie jegliche
#   Kommentare beliebig geaendert und entfernt und das Skript bearbeitet werden.
#
##################
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from time import gmtime, strftime
import time
import paho.mqtt.client as mqtt


##################
#
#   influxInit() stellt die Verbindung zur InfluxDB her.
#   Hier bedarf es keiner Aenderung solange sich am Server nichts aendert.
#   Die write_api ist aktuell nicht noetig, da die Daten derzeit per mqtt
#   geschrieben werden. Sollte das System dennoch auf die write_api umgestellt
#   werden, finden sich weitere Informationen auf:
#   https://www.influxdata.com/blog/getting-started-with-python-and-influxdb-v2-0/
#   und
#   https://github.com/influxdata/influxdb-client-python
#
##################
def influxInit():
    global influxclient
    influxclient = InfluxDBClient(url = "http://localhost:8086", token = "influxdbtoken", org = "ontop.hs-bochum.de")

    global write_api
    global query_api
    write_api = influxclient.write_api(write_options = SYNCHRONOUS)
    query_api = influxclient.query_api()


##################
#
#   influxRead() dient zum auslesen der Daten aus der InfluxDB.
#   query -> Hier wird der entsprechende Influx Befehl zum auslesen der Daten eingefügt.
#   result -> speichert das Ergebnis der InfluxDB.
#   results -> wie result, nur in tabellarischer Form, so dass die gewuenschten Ergebnisse
#   wie beim abstand aus den results rausgefiltert werden koennen.
#
##################
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

#   return abstand


##################
#
#   toLiter() dient ausschließlich zur bearbeitung der Daten
#   und kann beliebig bearbeitet und umbenannt werden
#
##################
def toLiter():
    global liter

    liter = (4320 * (1 - (abstand / 100) / 1.2))


##################
#
#   mqttWrite() verschickt die Daten per mqtt. Hier zu aendernde Daten sind:
#   TOPIC: entsprechnd dem Topic in welches die Daten gesendet werden.
#   mqttclient.username_pw_set: ("<Benutzername>", "<Passwort>") des verwendeten
#   mqtt Benutzers.
#   time und DATA: Wenn die Daten in die InfluxDB gesendet werden, kann time so
#   bleiben und in DATA muessen nur das Liter und die Variable liter geaendert
#   werden. Sind die Daten fuer die Nodes gedacht, folgt in Zukunft die
#   entsprechende Beschreibung.
#
##################
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


##################
#
#   Die Main Funktion: Hier muss nur der Name der toLiter() Funktion
#   entsprechend geaendert werden. Variablen muessen nicht uebergeben
#   werden, da (solange diese Konvention auch eingehalten wurde) jegliche
#   variablen als Globale Variablen deklariert sind (je nach verarbeitung
#   der Daten kann es sinnvoll sein einen Rueckgabewert aus influxRead()
#   zu erhalten).
#   time.sleep() stoppt das Programm in Sekunden.
#
##################
if __name__ == "__main__":

    influxInit()

    while(1):

        influxRead()

        toLiter()

        mqttWrite()

        time.sleep(300)

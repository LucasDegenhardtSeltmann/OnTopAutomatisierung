# OnTopAutomatisierung
Die Automatisierung im Rahmen des Softwareprojekts zur Bewässerung und Auswertung der Daten der Ontop Rooftop Farm Bochum

# Goals
## Weboberfläche für Öffentlichkeit
* Responsive Design
* Livestream der Webcam
* Graphen mit Interessanten Infos
  * Umsetzung mithilfe freier Bibliothek zB. charts.js
* Bildergallerie
* Über uns 

## Weboberfläche für OnTop Team
* Sammlung und Visualisierung aller erfassten Daten
  * Erstellung von Graphen anhand Ausgewählter Daten
  * Abruf der Daten in passendem Format ( csv, xls, pdf )
* Administrierung für Öffentlichkeits Ansicht

## App 
* Losgelöst von Website?
* Andere Inhalte als Website?
* Möglichkeit Website in simple App einzubauen mit offline Modus

## Server
* Webhosting
* Mqtt Broker
* Maria-/Postgresql Db
* P2P Stream oder Medienserver?
* Auswertung
  * Über Distanz Sensor Wasserstand und Verbrauch errechnen

## Sensorik
* Nodemcu V.3 
  - [x] -> Wurde bereits getestet
  - [x] Tasmota als Betriebssystem
  - [x] Mqtt Client zum senden der Daten
  - [ ] DeepSleep für optimales Energiemanagement
  - [ ] Magnetventil steuerung
  - [ ] Sensoren
    - [x] Ultraschall Distanz Sensor JSN-SR04t 
    - [x] Ultraschall Distanz Sensor HC-SR04 
    - [ ] Hygrometer 
    - [ ] Regen Sensor 
    - [ ] Temperatur Sensor DHT11
    - [ ] Luft/Gas Sensor MQ-2
    - [ ] Sonnenlicht Sensor

* RaspberryPi 4
  - [ ] Bereitstellung des Kamera Live Feeds
  - [ ] Fallback Db zur Sicherung der von Nodemcu gesendeten Daten gegen Internet Probleme
  - [ ] Massenspeicher für Kamera Bilder für zB. Zeitraffer
  - [ ] Pumpensteuerung ( evtl Obsolet )
  - [ ] Auslesen des Batteriemanagement Systems und der PV Anlage

* Beschaffte Elektronik
  * 5x Dc-Dc Buck Converter ( Downstepper ) 
  * 4x Ultraschall Distanz Sensor JSN-SR04t
  * 5x Nodemcu V.3
  * 6x 230V 1 Kanal Schalt Relais
  * 1x MQ-2 Gas Sensor
  * 1x DHT11 Temperatur Sensor
  * 1x Soil Moisture Sensor ( Hygrometer )

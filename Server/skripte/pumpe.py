import requests
import sys

argState = sys.arg[1]
requests.get('http://10.5.33.64/cs?c2=?&c1=power ' + str(argState))

##############
#
#   Skript mit Parametern ausführen: "pumpe.py on" bzw. "pumpe.py off"
#
##############

<?php
require '/app/vendor/autoload.php';

use InfluxDB2\Client;
use InfluxDB2\WriteType as WriteType;
//https://github.com/influxdata/influxdb-client-php

if ($_GET['PASSWORD'] == "ontopwetterstation1DV927KTX") {

	$organization = 'ontop.hs-bochum.de';
        $bucket = 'initial';
        $token = 'influxdbtoken';

        $client = new Client([
        	"url" => "http://influxdb:8086",
        	"token" => $token,
             	"bucket" => $bucket,
              	"org" => $organization,
                "precision" => InfluxDB2\Model\WritePrecision::S
        ]);

        $writeApi = $client->createWriteApi(); // QOS ~1 -> 5 Retries in the last 3 minutes.

	$weatherprefix = "";
	foreach ($_GET as $key => $value) {
	
		switch (substr($key, -3)) {
			case "mpf":
				// unit is in Fahrenheit (remove "f")
				send($writeApi, $weatherprefix.str_replace("mpf", "mp", $key), f2c($value));
				break;
			case "ptf":
				// unit is in Fahrenheit also (remove "f")
				send($writeApi, $weatherprefix.str_replace("ptf", "pt", $key), f2c($value));
				break;
			case "llf":
				// unit is in Fahrenheit also (remove "f")
				send($writeApi, $weatherprefix.str_replace("llf", "ll", $key), f2c($value));
				break;
			case "min":
				// unit is in inHg (remove "min")
				send($writeApi, $weatherprefix.str_replace("min", "", $key), inHG2hPa($value));
				break;
			case "nin":
				// unit is in inch (remove "in")
				send($writeApi, $weatherprefix.str_replace("nin", "n", $key), in2cm($value));
				break;
			case "mph":
				// unit is in mph (remove "mph")
				send($writeApi, $weatherprefix.str_replace("mph", "", $key), mph2kmh($value));
				break;
			case "utc":
				// unit is in UTC
				send($writeApi, $weatherprefix.$key, str2UTC($value)."");			
				break;
			default:
				// everything else: not a unit, or percent or string
				send($writeApi, $weatherprefix.$key, $value);
		}
	
		// flush remaining data
        	$client->close();
	}
} else {
	print "Error, wrong Password";
}



function send($writeApi, $item, $data) {
	if (is_numeric($data)) {

		$writeApi->write('Wetterstationen,Station='. $_GET['ID'] . ' ' . $item . '=' . $data . ' ' . time());
	}
}

function str2UTC($given_value) {
	return str_replace(" ", "T", $given_value);
}

function mph2kmh($given_value) {
	return '' . round( floatval($given_value) * 1.60934, 1);
}

function in2cm($given_value) {
	return '' . round( floatval($given_value) * 2.54, 1);
}

function inHG2hPa($given_value) {
	return '' . round( floatval($given_value) * 33.8639 , 1); //1 inHG = 3386,39 Pa, Bespielwert: 29.064 sollte ca 985 sein
}

function f2c($given_value) {
	return '' . round( (5.0 / 9 * (floatval($given_value) - 32 )), 1);
}
?>

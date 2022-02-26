<?php
require '/app/vendor/autoload.php';

use InfluxDB2\Client;
use InfluxDB2\WriteType as WriteType;
//https://github.com/influxdata/influxdb-client-php

#if ($_GET['PASSWORD'] == "") {

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

        $writeApi = $client->createWriteApi();

	$prefix = "";
	foreach (apache_request_headers() as $key => $value) {
	
		send($writeApi, $prefix.$key, $value);
	
		// flush remaining data
        	$client->close();
	}
#} else {
#	print "Error, wrong Password";
#}



function send($writeApi, $item, $data) {
	if (is_numeric($data)) {
		$onoff = array("OFF", "ON");
		$code = escapeshellcmd('python3 ./pumpeMqtt.py ' . $onoff[$data]);
		exec($code, $output, $error);

		#$writeApi->write('Control '. $item . '="' . $onoff[$data] . '" ' . time());
		$writeApi->write('Control '. $item . '=' . $data . ' ' . time());
	}
}
?>

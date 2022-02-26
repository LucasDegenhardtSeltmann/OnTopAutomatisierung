FROM bitnami/php-fpm

RUN apt-get update && apt-get install -y python3-pip && pip3 install paho-mqtt \
	&& rm -rf /var/lib/apt/lists/*

COPY --from=composer:latest /usr/bin/composer /usr/local/bin/composer
RUN composer require influxdata/influxdb-client-php



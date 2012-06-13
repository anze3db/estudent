#!/bin/bash

p="python2"

if [ "$1" == "db" ]
then
	rm estudent.db
	yes no | $p manage.py syncdb
	$p manage.py loaddata auth/fixtures/initial_data.json
fi

sudo $p manage.py runserver 0.0.0.0:80

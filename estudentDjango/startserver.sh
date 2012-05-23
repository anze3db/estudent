#!/bin/bash

if [ "$1" == "db" ]
then
	rm estudent.db
	yes no | python manage.py syncdb
	python loaddata auth/fixtures/initial_data.json
fi

python manage.py runserver

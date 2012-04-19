#!/bin/bash

if [ "$1" == "db" ]
then
	rm estudent.db
	yes no | python manage.py syncdb
fi

python manage.py runserver

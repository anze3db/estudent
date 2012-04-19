#!/bin/bash

if [ "$1" == "db" ]
then
	rm estudent.db
	python manage.py syncdb
fi

python manage.py runserver

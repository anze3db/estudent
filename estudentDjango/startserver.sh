#!/bin/bash

if [ "$1" == "db" ]
then
	rm student.db
	python manage.py syncdb
fi

python manage.py runserver

#!/bin/bash

dropdb mysite
createdb mysite
python manage.py syncdb
python manage.py loaddata data/demo4.json
python manage.py runserver 0.0.0.0:8000 



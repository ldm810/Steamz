#!/bin/bash

dropdb mysite
createdb mysite
python manage.py syncdb

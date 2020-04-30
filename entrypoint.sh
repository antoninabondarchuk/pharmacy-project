#!/bin/sh
python manage.py makemigrations
python manage.py migrate
./manage.py search_index --rebuild -f
python manage.py runserver 0.0.0.0:8000

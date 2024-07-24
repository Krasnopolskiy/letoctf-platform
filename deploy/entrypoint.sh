#!/bin/bash

echo "Apply database migrations"
./manage.py migrate

echo "Create superuser"
./manage.py createsuperuser --noinput

echo "Collect static files"
./manage.py collectstatic --noinput

echo "Start gunicorn server"
gunicorn -c gunicorn.conf.py backend.wsgi

exec "$@"

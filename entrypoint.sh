#!/bin/sh

echo 'Running Collectstatic...'
python manage.py collectstatic --no-input --settings=config.settings.production 

echo 'Apply Migrations...'
python manage.py waitForDb --settings=config.settings.production
python manage.py migrate --settings=config.settings.production


gunicorn --env DJANGO_SETTINGS_MODULE=config.settings.production config.wsgi:application --bind 0.0.0.0:7000

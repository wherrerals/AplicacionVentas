#!/bin/sh

#echo 'Running Collectstatic...'
#python manage.py collectstatic --no-input --settings=config.settings.production 

echo 'Apply Migrations...'
python manage.py waitForDb --settings=config.settings.production
python manage.py migrate --settings=config.settings.production


gunicorn --env DJANGO_SETTINGS_MODULE=config.settings.production config.wsgi:application --bind 0.0.0.0:7000
#gunicorn --env DJANGO_SETTINGS_MODULE=config.settings.production config.wsgi:application --bind 0.0.0.0:7000 --workers=17 --threads=4 --timeout 300 --log-level debug
#gunicorn --env DJANGO_SETTINGS_MODULE=config.settings.production config.wsgi:application \
#--bind 0.0.0.0:7000 --workers=16 --threads=4 --timeout=300 \
#--keep-alive 5 --max-requests 1000 --max-requests-jitter 100 --log-level debug


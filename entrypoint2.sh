#!/bin/sh

#echo 'Running Collectstatic...'
#python manage.py collectstatic --no-input --settings=config.settings.production 

echo 'Apply Migrations...'
python manage.py waitForDb --settings=config.settings.develop
python manage.py migrate --settings=config.settings.develop

echo 'Run server...'
python manage.py runserver --settings=config.settings.develop 0.0.0.0:8000 
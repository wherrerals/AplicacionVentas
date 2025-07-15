#!/bin/sh

echo "Esperando a que la base de datos esté lista..."
until nc -z db 3306; do
  echo "Esperando conexión con MySQL..."
  sleep 2
done

echo "Base de datos disponible, aplicando migraciones..."

python manage.py makemigrations --settings=config.settings.develop
python manage.py migrate --settings=config.settings.develop
python manage.py makemigrations datosLsApp --settings=config.settings.develop
python manage.py migrate datosLsApp --settings=config.settings.develop
python manage.py makemigrations taskApp --settings=config.settings.develop
python manage.py migrate taskApp --settings=config.settings.develop

echo "Migraciones completadas, iniciando el servidor..."

exec python manage.py runserver 0.0.0.0:8000 --settings=config.settings.develop
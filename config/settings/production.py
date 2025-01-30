import os

from dotenv import load_dotenv

from config.settings.base import *
from config.logging import *


load_dotenv(Path.joinpath(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['*'] #Cambiar por el dominio o ip de la maquina en la que se va a desplegar la aplicacion

#Configuracion para docker
""" DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'led_studio',
        'USER': 'root',
        'PASSWORD': 'Ea7hava5*',
        'HOST': 'db',
        'PORT': '4350',
    }
} """

#Database local Production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

STATIC_ROOT = Path.joinpath(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

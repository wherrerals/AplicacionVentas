import os

from dotenv import load_dotenv

from config.settings.base import *
from config.logging import *

load_dotenv(Path.joinpath(BASE_DIR, ".env"))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "192.168.3.42", "studio-go-dev"]

# Base service Layer
API_BASE_URL = os.environ.get("API_BASE_URL")
COMPANY_DB = os.environ.get("COMPANY_DB")
API_USERNAME = os.environ.get("API_USERNAME")
API_PASSWORD = os.environ.get("API_PASSWORD")

# Configuracion para DB docker
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
    }
}

# Configuracion para DB local

""" DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'led_studio',
        'USER':'root',
        'PASSWORD':'Ea7hava5*', #led_studio
        #'PASSWORD':'Ea7hava5}', #home
        #'PASSWORD':'qwerty', #nico
        #'HOST':'localhost',
        'PORT':'3306',
    }
}  """

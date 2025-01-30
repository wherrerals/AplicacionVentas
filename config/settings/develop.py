from config.settings.base import *
from config.logging import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-fexe1oq@sx@j&x3m#tw(#x(r!g32fylgea=whky=#ge^vn5f*h'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

ALLOWED_HOSTS = ['localhost','0.0.0.0:8000', '127.0.0.1']

""" #Configuracion para DB docker
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'led_studio',
        'USER': 'root',
        'PASSWORD': 'Ea7hava5*',
        'HOST': 'db',
        'PORT': '3306',
    }
}

#Configuracion para DB local """

DATABASES = {
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
} 

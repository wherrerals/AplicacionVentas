from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-fexe1oq@sx@j&x3m#tw(#x(r!g32fylgea=whky=#ge^vn5f*h'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

#DEBUG = False   

#En este se debe colocar la ip de la maquina en la que se esta trabajando o la ip de la maquina en la que se va a desplegar la aplicacion
ALLOWED_HOSTS = ['localhost','0.0.0.0:8000', '192.168.3.41', '192.168.3.42', '127.0.0.1']
#ALLOWED_HOSTS = []
#python manage.py runserver 192.168.3.41:8000


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'config',
    'datosLsApp',
    'logicaVentasApp',
    'showromVentasApp',
    'taskApp',

]

MIDDLEWARE = [
    'showromVentasApp.middleware.my_middleware.NoCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

#/Users/Cuervo/Documents/AplicacionVentas/showromVentasApp/templates/showromVentasApp
#/Users/nicor/Universidad/Practica/AplicacionVentas/showromVentasApp/templates/showromVentasApp
#/Users/William Herrera/Documents/Proyectoledstudio/AplicacionVentas/showromVentasApp/templates/showromVentasApp

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'showromVentasApp/templates/showromVentasApp')],
        #'DIRS': ['/Users/William Herrera/Documents/Proyectoledstudio/AplicacionVentas/showromVentasApp/templates/showromVentasApp'],
        #'DIRS': ['/Users/Cuervo/Documents/AplicacionVentas/showromVentasApp/templates/showromVentasApp'],
        #'DIRS': ['/Users/nicor/Universidad/Practica/AplicacionVentas/showromVentasApp/templates/showromVentasApp'],
        
        
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'showromVentasApp.context_processors.grupos_usuario',
                'showromVentasApp.context_processors.vendedor_codigo'
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATA_UPLOAD_MAX_NUMBER_FIELDS = None  # Permite un número ilimitado (no recomendado)

# Configuración de la base de datos local
""" 
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
}  """

# Configuración de Celery con RabbitMQ como broker
#localHost
#CELERY_BROKER_URL = 'amqp://guest:guest@localhost//'
#Docker
CELERY_BROKER_URL = 'amqp://guest:guest@rabbitmq:5672//'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'rpc://'

# Configuración de Celery con Redis como broker

# Configuración de rutas de tareas a colas específicas
CELERY_TASK_ROUTES = {
    'taskApp.tasks.sync_products': {'queue': 'sync_queue'},  # Asigna la tarea a una cola específica
}
# Otras configuraciones
CELERY_TASK_CREATE_MISSING_QUEUES = True

#Configuracion para docker
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'led_studio',         # Nombre de la base de datos
        'USER': 'root',               # Usuario de la base de datos
        'PASSWORD': 'Ea7hava5*',     # Contraseña del usuario
        'HOST': 'db',                 # Nombre del servicio en docker-compose
        'PORT': '3306',               # Puerto por defecto de MySQL
    }
} 

# Base service Layer
API_BASE_URL = 'https://182.160.29.24:50003/b1s/v1/'
COMPANY_DB = "TEST_LED_PROD"
#COMPANY_DB = "lED"
API_USERNAME = 'manager'
API_PASSWORD = '1245LED98'

# Base Vtex API
VTEX_APP_KEY = 'vtexappkey-ledstudiocl-AJHPCL'
VTEX_APP_TOKEN = 'WTEPUGSXUOIOMSAVTEIIJOCBMXTUZWTESEFDQHZSLHJZMJXAVHPGOPDKMUVMAPDBZXXDGDFJFNXCMFDNICGGSOCGFNKEHGSEWMEYRLHNCISFSILPJUYXMGKLZUXDKJLB'
VTEX_BASE_URL = 'https://ledstudiocl.myvtex.com/api/'


#python ./manage.py makemigrations showromVentasApp
#python ./manage.py sqlmigrate showromVentasApp 0001
#python ./manage.py migrate

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_TZ = True

LOGIN_REDIRECT_URL = '/ventas'
#LOGIN_REDIRECT_URL = '/Users/Cuervo/Documents/AplicacionVentas/showromVentasApp/templates/login'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



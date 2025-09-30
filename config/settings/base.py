from pathlib import Path
from kombu import Exchange, Queue
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# Application definition

BASE_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LOCAL_APPS = [
    "infrastructure",
    "apps.core",
    "config",
    "domain",
    "presentation",
    "taskApp",
    "logs",
    "uploadApp",
]

THIRD_APPS = []

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_APPS

BASE_MIDDLEWARE = [
    "presentation.middleware.my_middleware.NoCacheMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

LCOAL_MIDDLEWARE = []

THIRD_MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

MIDDLEWARE = BASE_MIDDLEWARE + LCOAL_MIDDLEWARE + THIRD_MIDDLEWARE


ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "presentation/templates/showromVentasApp")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "presentation.context_processors.grupos_usuario",
                "presentation.context_processors.vendedor_codigo",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATA_UPLOAD_MAX_NUMBER_FIELDS = None  # Permite un número ilimitado (no recomendado)

# Docker Config BROKER REDIS
CELERY_BROKER_URL = "amqp://admin:admin123@rabbitmq:5672//"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_BACKEND = "rpc://"

CELERY_TASK_QUEUES = (
    Queue("q.item.mw.studiogo", Exchange("ex.fanout.item.mw", type="fanout"), routing_key=""),
    Queue("q.item.mw.vtex", Exchange("ex.fanout.item.mw", type="fanout"), routing_key=""),
)

# Configuración de rutas de tareas a colas específicas
CELERY_TASK_ROUTES = {
    "taskApp.tasks.sync_products": {
        "queue": "q_products_in"
    },  # Asigna la tarea a una cola específica

    "taskApp.tasks.sync_products_receta": {
        "queue": "q_products_in_receta"
    },  # Asigna la tarea a una cola específica

        "taskApp.tasks.sync_products_importado": {
        "queue": "q_products_in_importado"
    },  # Asigna la tarea a una cola específica

    "taskApp.tasks.syncUser": {
        "queue": "q_clients_in"
    },  # Asigna la tarea a una cola específica

    "taskApp.tasks.prueba12": {
        "queue": "cola_productos"
    },  # Asigna la tarea a una cola específica
    
}

""" CELERY_TASK_ROUTES = {
    'taskApp.tasks.*': {'queue': 'default_queue'}  # Asigna todas las tareas a una cola predeterminada
}
 """
# Configuración para crear colas faltantes
CELERY_TASK_CREATE_MISSING_QUEUES = True


# Base Vtex API
VTEX_APP_KEY = os.environ.get("VTEX_APP_KEY")
VTEX_APP_TOKEN = os.environ.get("VTEX_APP_TOKEN")
VTEX_BASE_URL = os.environ.get("VTEX_BASE_URL")

# python ./manage.py makemigrations presentation
# python ./manage.py sqlmigrate presentation 0001
# python ./manage.py migrate

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "es-co"

TIME_ZONE = "America/Santiago"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

USE_I18N = True

USE_TZ = True

LOGIN_REDIRECT_URL = "/ventas"
# LOGIN_REDIRECT_URL = '/Users/Cuervo/Documents/AplicacionVentas/presentation/templates/login'

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

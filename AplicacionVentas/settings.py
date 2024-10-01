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

ALLOWED_HOSTS = []
#ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.3.41']
#python manage.py runserver 192.168.3.41:8000


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'AplicacionVentas',
    'datosLsApp',
    'logicaVentasApp',
    'showromVentasApp'    
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

ROOT_URLCONF = 'AplicacionVentas.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'AplicacionVentas.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'led_studio',
        'USER':'root',
        #'PASSWORD':'Ea7hava5}', #home
        #'PASSWORD':'Ea7hava5*', #led_studio
        'PASSWORD':'qwerty', #nico
        'HOST':'localhost',
        'PORT':'3306',
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



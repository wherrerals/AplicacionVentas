import os

from dotenv import load_dotenv

from config.settings.base import *
from config.logging import *


load_dotenv(Path.joinpath(BASE_DIR, ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = ["ventas.ledstudio.cl", "studio-go", "sgo2.ledstudio.cl"]

CSRF_TRUSTED_ORIGINS = ["https://sgo2.ledstudio.cl"]

# Base service Layer
API_BASE_URL = os.environ.get("API_BASE_URL")
COMPANY_DB = os.environ.get("COMPANY_DB")
API_USERNAME = os.environ.get("API_USERNAME")
API_PASSWORD = os.environ.get("API_PASSWORD")

# Google OAuth (login con cuentas @ledstudio.cl)
GOOGLE_OAUTH_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
GOOGLE_ALLOWED_DOMAIN = os.environ.get("GOOGLE_ALLOWED_DOMAIN", "ledstudio.cl")

# Google Sheets - Reporte Philips (philips_stock_transito, solo lectura)
GOOGLE_SA_CREDENTIALS = os.environ.get("GOOGLE_SA_CREDENTIALS")  # ruta al .json o JSON inline
PHILIPS_SHEET_ID = os.environ.get("PHILIPS_SHEET_ID")
PHILIPS_SHEET_RANGE = os.environ.get("PHILIPS_SHEET_RANGE", "Hoja 1")

# Detrás de nginx: confía en el header del proxy para armar redirect_uri en https
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# Database local Production
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

STATIC_ROOT = Path.joinpath(BASE_DIR, "staticfiles")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

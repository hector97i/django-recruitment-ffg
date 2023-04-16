import configparser
import json
import logging
import logging.config
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

VALID_RDBMS = ('sqlite3', 'postgresql')
CONFIG_FILE = os.getenv('CONFIG', 'config.json')
with open(os.path.join(BASE_DIR, CONFIG_FILE)) as cfg:
    CONFIG = json.load(cfg)

parser = configparser.ConfigParser()
parser.read(os.path.join(BASE_DIR, 'setup.cfg'))

# configuration
VERSION = parser['bumpversion']['current_version']
ENVIRONMENT = CONFIG['ENVIRONMENT']
SECRET_KEY = CONFIG['SECRET_KEY']
PROD = CONFIG['ENVIRONMENT'] == 'PRODUCTION'
DB = CONFIG['DB']
USE_S3 = CONFIG['AWS']['USE_S3']
DEBUG = CONFIG['DEBUG']
BASE_URL = CONFIG['BASE_URL']

ALLOWED_HOSTS = []
ALLOWED_ORIGINS_CONFIG = CONFIG['CORS']['ALLOWED_ORIGINS']
ALLOWED_ORIGINS_CONFIG.append(BASE_URL)

ALLOWED_HOSTS = CONFIG['ALLOWED_HOSTS']
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = CONFIG['CORS']['ALLOWED_ALL']
CORS_ALLOWED_ORIGINS = ALLOWED_ORIGINS_CONFIG
CSRF_TRUSTED_ORIGINS = ALLOWED_ORIGINS_CONFIG
CSRF_COOKIE_NAME = 'XSRF-TOKEN'

PROJECT_NAME = 'image_app'

# CORS_ALLOW_HEADERS = (
#     'xsrfheadername',
#     'xsrfcookiename',
#     'content-type',
#     'XSRF-TOKEN',
#     'x-csrftoken',
#     'X-CSRFToken',
#     'Authorization',
# )

LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(levelname)s] %(asctime)s %(message)s',
        },
        'console': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['console'],
        },
        'uvicorn': {
            'propagate': True,
        },
    },
}
logging.config.dictConfig(LOGGING)

logger = logging.getLogger(__name__)
logger.info(f'STARTING {ENVIRONMENT} SERVER. v{VERSION}')

if DB['RDBMS'] not in VALID_RDBMS:
    logger.error('DATABASE RBMS NOT ALLOWED')
    sys.exit(2)
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
    'storages',
    'images',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'image_app.urls'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'api.pagination.BasePagination',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Images API v1',
    'DESCRIPTION': 'Django/DRF REST API for uploading and serving images',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'image_app.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': f'django.db.backends.{DB["RDBMS"]}',
        'NAME': BASE_DIR / 'db.sqlite3' if DB['RDBMS'] == 'sqlite3' else DB['NAME'],
        'USER': DB['USER'],
        'PASSWORD': DB['PASSWORD'],
        'HOST': DB['HOST'],
        'PORT': DB['PORT'],
    },
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Set boto3 auth env variables
os.environ['AWS_DEFAULT_REGION'] = CONFIG['AWS']['REGION_NAME']
os.environ['AWS_ACCESS_KEY_ID'] = CONFIG['AWS']['ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY'] = CONFIG['AWS']['SECRET_ACCESS_KEY']
STORAGES = {
    'default': {'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage'},
    "staticfiles": {"BACKEND": "storages.backends.s3boto3.S3StaticStorage"},
}
# aws
AWS_ACCESS_KEY_ID = CONFIG['AWS']['ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = CONFIG['AWS']['SECRET_ACCESS_KEY']
AWS_S3_REGION_NAME = CONFIG['AWS']['REGION_NAME']
AWS_STORAGE_BUCKET_NAME = CONFIG['AWS']['STORAGE_BUCKET_NAME']
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

if USE_S3:
    logger.warning('USING S3 AS STATIC PROVIDER')
    MEDIA_LOCATION = 'media'
    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, CONFIG['STATIC_ROOT_PATH'])
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, CONFIG['MEDIA_ROOT_PATH'])

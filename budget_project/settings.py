from pathlib import Path

# import environ # https://django-environ.readthedocs.io/en/latest/index.html - to read .env
import os

import google.auth
from google.cloud import secretmanager

# env = environ.Env(
#     # set casting, default value
#     DEBUG=(bool, False)
# )

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
# environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = env("SECRET_KEY")
# SECRET_KEY = os.environ.get('SECRET_KEY', '')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

# ALLOWED_HOSTS = []

#############################
### ENVIRONMENT VARIABLES ###
#############################
try:
    client = secretmanager.SecretManagerServiceClient()
    name = "projects/budgettracker-399813/secrets/django_settings/versions/latest"
    payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")
    payload = payload.split('\n')
    ENVIRONMENT = 'prod'
 
    for p in payload: # Each line in payload looks like GOOGLE_CLOUD_PROJECT=my-project-id.
        if p.startswith('GOOGLE_CLOUD_PROJECT'): 
            GOOGLE_CLOUD_PROJECT = p.split('=')[1]
 
        if p.startswith('DATABASE_HOST'):
            DATABASE_HOST = p.split('=')[1]
 
        if p.startswith('DATABASE_NAME'):
            DATABASE_NAME = p.split('=')[1]
 
        if p.startswith('DATABASE_USER'):
            DATABASE_USER = p.split('=')[1]
 
        if p.startswith('DATABASE_PASSWORD'):
            DATABASE_PASSWORD = p.split('=')[1]
             
        if p.startswith('SECRET_KEY'):
            result = ''
            for i, s in enumerate(p.split('=')):
                if i != 0:
                    result += s
            SECRET_KEY = result
      
    # Successfully loading secrets manager means production environment.
    
    DEBUG = False
 
except google.auth.exceptions.DefaultCredentialsError:
    ENVIRONMENT = 'dev'
    DEBUG = True
    ALLOWED_HOSTS = ['*']
    SECRET_KEY = os.environ.get('SECRET_KEY', '')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # my apps
    'budget_app',
    'home',
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

ROOT_URLCONF = 'budget_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'static/templates',
        ],
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

WSGI_APPLICATION = 'budget_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if ENVIRONMENT == 'prod':
    # Production, Google CloudSQL DB.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': DATABASE_NAME,
            'USER': DATABASE_USER,
            'PASSWORD': DATABASE_PASSWORD,
            'HOST': 'DATABASE_HOST',
        }
    }
else:
    if os.environ.get('USE_CLOUD_PROXY', False) == 'true':
        print('Connecting to Google Cloud SQL proxy…')
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.environ.get('CLOUD_PROXY_DB', ''),
                'USER': os.environ.get('CLOUD_PROXY_USER', ''),
                'PASSWORD': os.environ.get('CLOUD_PROXY_PASSWORD', ''),
                'HOST': 'budget_project_cloudsql_proxy',
                'PORT': 5432,
            }
        }
    else:
        print('Connect to DB: LOCAL POSTGRES')
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'postgres',
                'USER': 'postgres',
                'PASSWORD': 'postgres',
                'HOST': 'pgdb',
                'PORT': 5432,
            }
        }


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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Almaty'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'home'

USE_THOUSAND_SEPARATOR = True


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Use this for testing goal to output email to console:
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
# EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')


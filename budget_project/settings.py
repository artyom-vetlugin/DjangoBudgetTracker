from pathlib import Path

# import environ # https://django-environ.readthedocs.io/en/latest/index.html - to read .env
import os

import google.auth
from google.cloud import secretmanager


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/


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
 
        if p.startswith('GS_BUCKET_NAME'):
            GS_BUCKET_NAME = p.split('=')[1]
        
        if p.startswith('DATABASE_HOST'):
            DATABASE_HOST = p.split('=')[1]
 
        if p.startswith('DATABASE_NAME'):
            DATABASE_NAME = p.split('=')[1]
 
        if p.startswith('DATABASE_USER'):
            DATABASE_USER = p.split('=')[1]
 
        if p.startswith('DATABASE_PASSWORD'):
            DATABASE_PASSWORD = p.split('=')[1]
             
        if p.startswith('CLOUDRUN_SERVICE_URL'):
            CLOUDRUN_SERVICE_URL = p.split('=')[1]
        
        if p.startswith('SECRET_KEY'):
            result = ''
            for i, s in enumerate(p.split('=')):
                if i != 0:
                    result += s
            SECRET_KEY = result
      
    # Successfully loading secrets manager means production environment.
    
    DEBUG = False

    if CLOUDRUN_SERVICE_URL:
        ALLOWED_HOSTS = [CLOUDRUN_SERVICE_URL]
        CSRF_TRUSTED_ORIGINS = ['https://' + CLOUDRUN_SERVICE_URL]
        SECURE_SSL_REDIRECT = True
        SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
 
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql'
    }
}
if ENVIRONMENT == 'prod':
    # Production, Google CloudSQL DB.
    DATABASES['default']['NAME'] = DATABASE_NAME
    DATABASES['default']['USER'] = DATABASE_USER
    DATABASES['default']['PASSWORD'] = DATABASE_PASSWORD
    DATABASES['default']['HOST'] = DATABASE_HOST
else:
    DATABASES['default']['PORT'] = 5432
    if os.environ.get('USE_CLOUD_PROXY', False) == 'true':
        # Local, Google CloudSQL Proxy DB.
        print('Connect to DB: GOOGLE CLOUD PROXY')
        DATABASES['default']['NAME'] = os.environ.get('CLOUD_PROXY_DB', '')
        DATABASES['default']['USER'] = os.environ.get('CLOUD_PROXY_USER', '')
        DATABASES['default']['PASSWORD'] = os.environ.get('CLOUD_PROXY_PASSWORD', '')
        DATABASES['default']['HOST'] = 'budget_project_cloudsql_proxy'
    else:
        # Local, Postgres DB.
        print('Connect to DB: LOCAL POSTGRES')
        DATABASES['default']['NAME'] = 'postgres'
        DATABASES['default']['USER'] = 'postgres'
        DATABASES['default']['PASSWORD'] = 'postgres'
        DATABASES['default']['HOST'] = 'pgdb'

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
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

if ENVIRONMENT == 'prod':
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    GS_DEFAULT_ACL = "publicRead"
else:
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


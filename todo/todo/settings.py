"""
Django settings for todo project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-edd%1zluv+fyibd+7q^p2%l9xp+29bdslixk^+93&fyh0a_-%8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    
    'app',
    'django_celery_results',
    'django_celery_beat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#File Based Session
#SESSION_ENGINE = 'django.contrib.sessions.backends.file'
#SESSION_FILE_PATH = 'os.path.join(BASE_DIR, '')'

ROOT_URLCONF = 'todo.urls'
AUTH_USER_MODEL = "app.MyCustomModel"
#LOGIN_URL = 'mytodo/login/'
AUTHENTICATION_BACKENDS = ['app.auth_backends.EmailBackend']
#SESSION_ENGINE =[ "django.contrib.sessions.backends.cache"]

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

WSGI_APPLICATION = 'todo.wsgi.application'
# ASGI_APPLICATION = 'todo.asgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default' : {
#         'ENGINE' : 'django.db.backends.postgresql_psycopg2',
#         'NAME' : 'account',      #database name
#         'USER' : 'postgres',     #user name
#         'PASSWORD' : 'satya',    #db password
#         'HOST' : 'localhost',
#         'PORT' : '5432',
#     }
# }

# CACHES = {
#     'default': {
#       'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#       'LOCATION': 'C:/Users/vikra/OneDrive/Desktop/Todo3 eith email/todo/app/django_cache',
#       'TIMEOUT' : 60
#
#     }



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

#DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#managing media
MEDIA_ROOT = os.path.join('BASE_DIR', 'media')
MEDIA_URL = '/media/'

#SMTP SETTINGS
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "satya.prakash1132@gmail.com" 
DEFAULT_FROM_EMAIL = 'satya.prakash1132@gmail.com'
EMAIL_HOST_PASSWORD = "amsixzqijfqqyfty"
SERVER_EMAIL = "satya.prakash1132@gmail.com"
#DEFAULT_FROM_EMAIL = 'Testing <satya.prakash1132@gmail.com>'


#PASSWORD_RESET_TIMEOUT_DAYS
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("127.0.0.1", 6379)],
#         },
#     },
# }
CELERY_BROKEN_URL = 'redis://127.0.0.1:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'


CELERY_RESULT_BACKEND = 'django-db'

#celery-beat

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
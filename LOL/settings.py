# -*- coding: UTF-8 -*-
"""
Django settings for LOL project.

Generated by 'django-admin startproject' using Django 1.9.13.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ee-i1kqnx9=pc317dz2kr#54p@m@svtt)*!x=qjg^6ci(saa!j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'job',
    'business',
    'cmdb',
    'custag',
    'djcelery',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'LOL.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'LOL.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'lol',  # Or path to database file if using sqlite3.
        'USER': 'root',  # Not used with sqlite3.
        'PASSWORD': 'my-secret-pw',  # Not used with sqlite3.
        'HOST': '127.0.0.1',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
        # 'OPTIONS': {"init_command": "SET foreign_key_checks = 0;",},
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
###################非django默认内容###########################


def MyMkDir(_dir):
    if not os.path.exists(_dir):
        os.mkdir(_dir)


LOG_FILE_DIR = os.path.join(BASE_DIR, 'logs')
print(LOG_FILE_DIR)
MyMkDir(LOG_FILE_DIR)

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
LOGIN_REDIRECT_URL = '/index/'

############################################
import djcelery

djcelery.setup_loader()
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = False
BROKER_URL = 'redis://localhost:6379'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'  # 定时任务
# CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYD_MAX_TASKS_PER_CHILD = 3  # 每个worker最多执行3个任务就会被销毁，可防止内存泄露
############################################
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'standard',
        },
        'job_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_FILE_DIR, 'job.log'),
            'formatter': 'standard',
        },
        'business_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_FILE_DIR, 'business.log'),
            'formatter': 'standard',
        },
        'log_record_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_FILE_DIR, 'log_record.log'),
            'formatter': 'standard',
        },
        'cmdb_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_FILE_DIR, 'cmdb.log'),
            'formatter': 'standard',
        },
        'scheduled_tasks_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_FILE_DIR, 'scheduled_tasks.log'),
            'formatter': 'standard',
        },
        'business_query_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_FILE_DIR, 'business_query.log'),
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'job': {
            'handlers': ['job_handler'],
            'level': 'INFO',
            'propagate': False
        },
        'business': {
            'handlers': ['business_handler'],
            'level': 'INFO',
            'propagate': False
        },
        'log_record': {
            'handlers': ['log_record_handler'],
            'level': 'INFO',
            'propagate': False
        },
        'cmdb': {
            'handlers': ['cmdb_handler'],
            'level': 'INFO',
            'propagate': False
        },
        'scheduled_tasks': {
            'handlers': ['scheduled_tasks_handler'],
            'level': 'INFO',
            'propagate': False
        },
        'business_query': {
            'handlers': ['business_query_handler'],
            'level': 'INFO',
            'propagate': False
        },
    }
}
##############################################
try:
    from .settings_dev import *
except Exception as e:
    print e.message
    print u"=" * 20 + u'正式环境' + u"=" * 20

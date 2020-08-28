"""
Django settings for GatewayServer project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pzx0t2d%%(2i_-tg2^5v3@)4kgihqx8#*l!m+6v*qtjj@zjwuv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'GWS.apps.GwsConfig',
    # 'werkzeug_debugger_runserver',
    # 'django_extensions',
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

ROOT_URLCONF = 'GatewayServer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'GatewayServer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'gws_test1',
#         'USER': 'postgres',
#         'PASSWORD': '123456',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# SECURE_SSL_REDIRECT = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
AUTH_USER_MODEL = 'GWS.UserProfile'

STATIC_URL = '/static/'
# STATIC_ROOT = 'static'  # # 新增行
# STATICFILES_DIRS = [
#   os.path.join(BASE_DIR, '/static/'),  # # 修改地方
# ]
#
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

LOGIN_URL = '/login/'

# CMD_header = {
#     "get_data_manually": "get_data_manually",
#     "gwdata": "gwdata",
#     "gwntid": "gwntid",
#     "sync_sensors": "sync_sensors",
#     "update_sensor": "update_sensor",
#     "add_sensor": "add_sensor",
#     "remove_sensor": "remove_sensor",
#     "server_status": "server_status",
#     "update_gateway": "update_gateway",
#     "add_gateway": "add_gateway",
#     "heart_ping": "heart_ping",
#     "pause_sensor": "pause_sensor",
#     "resume_sensor": "resume_sensor",
#
# }

heart_time = {'minutes': 0, 'seconds': 30}

# EMQ X SETTINGS
# MQTT_HOST = "121.36.220.210"
MQTT_HOST = "127.0.0.1"
MQTT_USERNAME = 'ORISONIC'
MQTT_PASSWORD = 'ORISONIC2020'

# crtPath = BASE_DIR + r"\crt_47.93.190.54"
crtPath = BASE_DIR + r"\crt_192.168.0.44"

ca_certs = "%s\ca\MyRootCA.pem" % crtPath
certfile = "%s\client\MyClient1.pem" % crtPath
keyfile = "%s\client\MyClient1.key" % crtPath

# ca_certs = "%s/ca/MyRootCA.pem" % crtPath
# certfile = "%s/client/MyClient1.pem" % crtPath
# keyfile = "%s/client/MyClient1.key" % crtPath


# aliyunsdkcore
accessKeyId = "accessKeyId"
accessSecret = "accessSecret"
TemplateCode = "TemplateCode"


# 错误日志
ERROR_LOG_FILE = os.path.join(BASE_DIR, "log", 'error.log')
# 运行日志
RUN_LOG_FILE = os.path.join(BASE_DIR, "log", 'run.log')




"""
Django settings for THUONGMAIDIENTU project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path


import oauth2_provider.contrib.rest_framework
from django.conf.global_settings import AUTH_USER_MODEL, MEDIA_ROOT

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-r5hciu=2zcdsm=x@kuixs^btx)5!l3&u31hm4#1_k8i9@&itsg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'San_HNT.apps.SanHntConfig',
    'rest_framework',
    'oauth2_provider',
    'corsheaders',
    'cloudinary',
    'cloudinary_storage',
    'drf_yasg',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
]
CORS_ALLOW_ALL_ORIGINS = True

ALLOWED_HOSTS = ['192.168.1.154', '192.168.1.1', '192.168.196.1', '127.0.0.1', '10.17.39.150']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'THUONGMAIDIENTU.urls'

AUTH_USER_MODEL = 'San_HNT.User'

MEDIA_ROOT = f'{BASE_DIR}/San_HNT/static/'


OAUTH2_PROVIDER = { 'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore' }

client_id ='kmFU6SfP5tlxLl32F40efKFzunsnQxqfAwxpdjTI'
client_secret= '9hXxO3WhrLLCG1D8cZ9Ythz7UfGbp4GUT8nFZcGxICgb0QHodXAbudLLwb4R74RJZoCrhIEwXVJenHvHUzikyNmSAKMMWUuKfHkFEyXlWuiKoR0ekqjuLIB7oiQyAF2B'


REST_FRAMEWORK ={
    'DEFAULT_AUTHENTICATION_CLASSES':  ['oauth2_provider.contrib.rest_framework.OAuth2Authentication',]

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

WSGI_APPLICATION = 'THUONGMAIDIENTU.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'santhuongmaidientu',
        'USER': 'root',
        'PASSWORD': '594362',
        'HOST': ''
    }
}

import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    cloud_name = "dxw8gtpd8",
    api_key = "732195383843196",
    api_secret = "GwsB2gkTHCD5T0CEHwrO2BpKtzc", # Click 'View API Keys' above to copy your API secret
    secure=True
)


DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

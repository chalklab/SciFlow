"""
Django settings for sciflow project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from sciflow.localsettings import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xzdi*3p9062t$u9yz5jehu2xsjc=9!+75hlic=-3k^=k^!ssch7rf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['sds.coas.unf.edu', '127.0.0.1', 'localhost']

# cors setup
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ['http://127.0.0.1:8000']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'corsheaders',
    'rest_framework',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'crispy_forms',
    'contexts',
    'datasets',
    'substances',
    'workflow',
    'datafiles',
    'debug_toolbar',
    'quads',
    'targets'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

ROOT_URLCONF = 'sciflow.urls'

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

WSGI_APPLICATION = 'sciflow.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

LOCALDB = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

UNFDB = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sciflow',
        'USER': sfuser,
        'PASSWORD': sfpass,
        'HOST': '127.0.0.1',
        'PORT': '3307'
    },
    'trc': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'trcv2_clean',
        'USER': 'trc',
        'PASSWORD': 'trc42',
        'HOST': '127.0.0.1',
        'PORT': '3307'
    }
}

DATABASES = UNFDB

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
ua = 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
ml = 'django.contrib.auth.password_validation.MinimumLengthValidator'
cp = 'django.contrib.auth.password_validation.CommonPasswordValidator'
np = 'django.contrib.auth.password_validation.NumericPasswordValidator'
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': ua}, {'NAME': ml}, {'NAME': cp}, {'NAME': np}
]

# database autofield selection (Django 3.2)
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


# Crispy settings

CRISPY_TEMPLATE_PACK = "bootstrap4"


# graphdb ingest directory on sds
gdrivesds = "/Users/n00002621/GoogleDrive/Research/sciflow"


STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)

authorized_users = [
    'cweb1182@gmail.com',
    'jaredracicot@gmail.com',
    'stuartjchalk@gmail.com',
    'n01448636@gmail.com',
    'markaidestine@gmail.com',
    'abdurazikd1@gmail.com'
]

# Debug toolbar settings

INTERNAL_IPS = [
    '127.0.0.1',
]

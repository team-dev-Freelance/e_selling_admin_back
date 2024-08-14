"""
Django settings for e_selling_admin_back project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

BASE_DIR_MEDIA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR_MEDIA, 'media')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# settings.py
AUTH_USER_MODEL = 'utilisateur.Utilisateur'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^k#(#tk5!gslwc=aj6x=vubs5n%m-+)u(+$gn*texj50p8aiv8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'esellingadminback-production.up.railway.app']
CORS_ALLOWED_ORIGINS = ['http://localhost:4200']
CSRF_TRUSTED_ORIGINS = ['http://localhost:4200', 'https://esellingadminback-production.up.railway.app']

# CORS_ALLOW_HEADERS = ['content-type', 'authorization']
# CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']

APPEND_SLASH = False

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt',
    'rest_framework',
    'django_extensions',
    # 'member',
    'organisation',
    'cart',
    'rule',
    'privilegies',
    'article',
    # 'client',
    'categorie',
    # 'acheter',
    'utilisateur',
    'corsheaders',
]

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'e_selling_admin_back.urls'

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

WSGI_APPLICATION = 'e_selling_admin_back.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'selling_db',  # Nom de votre base de données
#         'USER': 'root',  # Votre nom d'utilisateur MySQL
#         'PASSWORD': 'koire',  # Votre mot de passe MySQL
#         'HOST': 'localhost',  # L'hôte de votre base de données
#         'PORT': '3306',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_DATABASE', 'railway'),
        'USER': os.environ.get('MYSQL_USER', 'root'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD', 'DZldFrYNLmcUJuCcCeziRVmsSFsODDEt'),
        'HOST': os.environ.get('MYSQL_HOST', 'viaduct.proxy.rlwy.net'),
        'PORT': os.environ.get('MYSQL_PORT', '29245'),
    }
}


# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ),
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated',
#     ),
# }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # 'django.middleware.common.CommonMiddleware',
]

# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
#     'ROTATE_REFRESH_TOKENS': False,
#     'BLACKLIST_AFTER_ROTATION': True,
#     'UPDATE_LAST_LOGIN': False,
#     'ALGORITHM': 'HS256',
#     'SIGNING_KEY': SECRET_KEY,
#     'VERIFYING_KEY': None,
#     'AUTH_HEADER_TYPES': ('Bearer',),
#     'USER_ID_FIELD': 'id',
#     'USER_ID_CLAIM': 'user_id',
#     'AUTH_TOKEN_CLASSES': ('access',),
#     'TOKEN_USER_CLASS': None,
# }

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Par exemple, 60 minutes
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),    # Par exemple, 1 jour
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=60),
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

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

# import cloudinary
# import cloudinary.uploader
# import cloudinary.api

# import cloudinary
# import cloudinary.uploader
# from cloudinary.utils import cloudinary_url

# SMS
#ORANGE_CLIENT_ID = '82Ubo9gpMnQrDtTccL7Yz1cWsJhBO0ts'
#ORANGE_CLIENT_SECRET = 'votre_client_secret'
#ORANGE_PHONE_NUMBER = '237XXXXXXXX'
#ORANGE_SMS_API_URL = 'https://api.orange.com/smsmessaging/v1/outbound/tel%3A%2B{{ORANGE_PHONE_NUMBER}}/requests'



# Configuration
# cloudinary.config(
#     cloud_name="doi8u5nki",
#     api_key="371996395793828",
#     api_secret="ensTEAUBn3duPLjDt13vifMxTB8",  # Click 'View API Keys' above to copy your API secret
#     secure=True
# )

# # Upload an image
# upload_result = cloudinary.uploader.upload("https://res.cloudinary.com/demo/image/upload/getting-started/shoes.jpg",
#                                            public_id="shoes")
# print(upload_result["secure_url"])
#
# # Optimize delivery by resizing and applying auto-format and auto-quality
# optimize_url, _ = cloudinary_url("shoes", fetch_format="auto", quality="auto")
# print(optimize_url)
#
# # Transform the image: auto-crop to square aspect_ratio
# auto_crop_url, _ = cloudinary_url("shoes", width=500, height=500, crop="auto", gravity="auto")
# print(auto_crop_url)

# CLOUDINARY_URL = 'cloudinary://371996395793828:ensTEAUBn3duPLjDt13vifMxTB8@doi8u5nki'
# CLOUDINARY_URL = 'cloudinary://371996395793828:ensTEAUBn3duPLjDt13vifMxTB8@doi8u5nki'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

BASE_DIR_MEDIA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR_MEDIA, 'media')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# settings.py
AUTH_USER_MODEL = 'utilisateur.Utilisateur'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'wawouam@gmail.com'
EMAIL_HOST_PASSWORD = 'npdd sdvc moaq ozal '

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^k#(#tk5!gslwc=aj6x=vubs5n%m-+)u(+$gn*texj50p8aiv8'
DB_NAME='railway'
DB_HOST='autorack.proxy.rlwy.net'
DB_PORT=13977
DB_PASSWORD='pItdcCsnoziKMtuCpnZvyDwvNjWLxJVM'
DB_USERNAME='root'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"

    
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,102.220.19.164,'http://e-commerce.enspm.univ-maroua.cm'").split(",")

CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',
    'http://102.220.19.164:8082',
    'https://web-production-1ab04.up.railway.app',
    'http://102.220.19.164:4200',
    'https://esellingadminfront-production.up.railway.app',
    'http://102.220.19.164:3000',
    'http://127.0.0.1:8000',
    'http://localhost:46759',
    'http://e-commerce.enspm.univ-maroua.cm'

]

CSRF_TRUSTED_ORIGINS = [
    'http://102.220.19.164:3000',
    'http://localhost:4200',
    'http://102.220.19.164:8082',
    'https://web-production-1ab04.up.railway.app',
    'http://e-commerce.enspm.univ-maroua.cm',
    'https://esellingadminfront-production.up.railway.app',
    'http://102.220.19.164:4200',
    'http://127.0.0.1:8000',
    'http://localhost:46759',
]

APPEND_SLASH = False

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

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
    'order',
    'rule',
    'privilegies',
    'article',
    # 'client',
    'categorie',
    # 'acheter',
    'utilisateur',
    'passwordResetCode',
    'corsheaders',
    'smsorange'
]

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
#         'NAME': os.getenv('DB_NAME'),
#         'USER': os.getenv('DB_USERNAME'),
#         'PASSWORD': os.getenv('DB_PASSWORD'),
#         'HOST': os.getenv('DB_HOST'),
#         'PORT': os.getenv('DB_PORT'),
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'selling_db',
#         'USER': 'root',
#         'PASSWORD': 'koire',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'selling_db',
        'USER': 'root',
        'PASSWORD': 'koire',
        'HOST': '102.220.19.164',
        'PORT': '3307',
        # 'OPTIONS': {
        #     'connect_timeout': 60,  # Augmenter le timeout de connexion
        #     'init_command': "SET SESSION wait_timeout = 28800",
        # }
    }
}

# DATABASES = {
#     'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'selling_db',
#        'USER': 'root',
#        'PASSWORD': '',
#        'HOST': 'localhost',
#        'PORT': '3306',

#    }
# }

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ),
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated',
#     ),
# }

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#         # 'rest_framework.permissions.AllowAny',
#     ),
# }

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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

# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Par exemple, 60 minutes
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  # Par exemple, 1 jour
#     'ROTATE_REFRESH_TOKENS': False,
#     'BLACKLIST_AFTER_ROTATION': True,
#     'UPDATE_LAST_LOGIN': False,
#
#     'ALGORITHM': 'HS256',
#     'SIGNING_KEY': SECRET_KEY,
#     'VERIFYING_KEY': None,
#     'AUDIENCE': None,
#     'ISSUER': None,
#
#     'AUTH_HEADER_TYPES': ('Bearer',),
#     'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
#     'USER_ID_FIELD': 'id',
#     'USER_ID_CLAIM': 'user_id',
#     'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
#
#     'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
#     'TOKEN_TYPE_CLAIM': 'token_type',
#     'JTI_CLAIM': 'jti',
#
#     'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
#     'SLIDING_TOKEN_LIFETIME': timedelta(minutes=60),
# }

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

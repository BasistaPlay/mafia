"""
Django settings for MafiaWebsite project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@3c25l29hzhu$811**&-lr955g-m49e6d0*)td#9#g6#ba%w$#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'daphne',
    'django.contrib.staticfiles',
    'django_extensions',



    # my apps

    'mainpage',
    'GameRoom',
    'game',



    # alauth apps

    'django.contrib.messages',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',

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
ROOT_URLCONF = 'MafiaWebsite.urls'

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

WSGI_APPLICATION = 'MafiaWebsite.wsgi.application'
ASGI_APPLICATION = 'MafiaWebsite.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mafia_website',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
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

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-en'

TIME_ZONE = 'Europe/Riga'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# jazzmitn settings(admin page)

JAZZMIN_SETTINGS = {
    'site_title': 'Mafia',
    'site_header': 'Game',
    'site_logo': '',
    'welcome_sign': 'Welcome to Mafia',  # Customize the welcome message
    'show_sidebar': True,  # Show the sidebar menu
    'navigation_expanded': True,  # Expand all sections in the sidebar menu
    'hide_apps': ["""'sites'"""],  # Hide specific apps from the admin sidebar
    'show_ui_builder': False,  # Hide the UI Builder link in the top menu
    'topmenu_links': [],  # Remove any custom links from the top menu
    'usermenu_links': [],  # Remove any custom links from the user menu
    'theme': 'home',  # Use the 'home' theme style
    'icons': {  # Customize icons for specific models or apps
        'app.Model': 'fas fa-icon',  # Replace 'app.Model' with your desired model
        'auth.User': 'fas fa-user',
        'gameroom.GameRoom': 'fas fa-door-open',
        'gameroom.Player': 'fas fa-users',
        'game.role': 'fas fa-star',
        'game.location': 'fas fa-map-marker',
        'mainpage.Profile': 'fas fa-id-card',

    },
    # ... other customization options ...
}

SITE_ID = 1


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.privateemail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'team@mafiawebsite.xyz'
EMAIL_HOST_PASSWORD = 'Edvards!@#123'
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = 'WebsiteTitle <team@mafiawebsite.xyz>'
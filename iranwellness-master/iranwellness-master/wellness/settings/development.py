
import os
from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ga+6r%6p9d%s*t4j@dz-j857gs7b0wwd=7d+^_@$ki^n5#m^a4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # local apps
    'authapp.apps.AuthappConfig',
    'index.apps.IndexConfig',
    'manager.apps.ManagerConfig',
    'news.apps.NewsConfig',
    'quiz.apps.QuizConfig',
    'reservation.apps.ReservationConfig',
    'services.apps.ServicesConfig',
    'shop.apps.ShopConfig',
    'specialists.apps.SpecialistsConfig',
    'ticket.apps.TicketConfig',
    'zarinpal.apps.ZarinpalConfig',
    # third-party apps
    'debug_toolbar',
    'django_filters',
    'django_jalali',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'wellness.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'wellness/templates',
            'index/templates',
            'authapp/templates',
            'services/templates',
            'reservation/templates',
            'quiz/templates',
            'ticket/templates',
            'news/templates',
            'shop/templates',
            'zarinpal/templates',
            'manager/templates',
            'specialists/templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
                'custom_file_field_tags': 'index.templatetags.custom_file_field_tags',
            }
        },
    },
]

WSGI_APPLICATION = 'wellness.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


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

LANGUAGE_CODE = 'fa'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True


#----------------------------------------------------------------------------------
#                            STATIC and MEDIA PATH
#----------------------------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

#----------------------------------------------------------------------------------


#----------------------------------------------------------------------------------
#                                LOGIN SETTINGS
#----------------------------------------------------------------------------------
LOGIN_REDIRECT_URL='/dashboard/'
LOGIN_URL ='/login/'

#----------------------------------------------------------------------------------


#----------------------------------------------------------------------------------
#                             django rest framework settings
#----------------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
}

#-----------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------
#                                django-debug-toolbar settings
#-----------------------------------------------------------------------------------
INTERNAL_IPS = [
    '127.0.0.1',
]

#------------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
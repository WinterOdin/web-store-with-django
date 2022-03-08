from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SITE_ID = 1

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')j)!m=8vewybi=nsrw&l5#)4#sacu++ltc9y(f+kq-)3eq^+8f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

STRIPE_PUBLIC_KEY = 'pk_test_51HEYqgEPUz3ZLxoXDOQ1eA9kElSC05FZx8cUrgpbtmLTDTjVR3WSIv8MNvK5C5AFtpY1eTCPbwQ1uAdOA34lHXYX00aqD5lm9W'
STRIPE_PRIVATE_KEY = 'sk_test_51HEYqgEPUz3ZLxoXSeaw8yhcTQK7MNGnk57g7O6juKU4L4SSUbjNgE0vVjCEzehX2DZMLpPSFha9sMBEXeLXPRS100v3J11TXs'

# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'authentication',
    'Control_Panel',
    'mainpage',
    'ckeditor',
    'ckeditor_uploader',
    'taggit',
    'user',
    
]
CKEDITOR_UPLOAD_PATH = 'uploads/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'public_python.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'public_python.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':'cryptoTech',
        'USER':'postgres',
        'PASSWORD':'M@rcel10',
        'HOST':'localhost',
        'PORT':'5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'pl'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]
LANGUAGES = [
    ('en','English'),
    ('pl','Polish'),

]


STATIC_ROOT = os.path.join(BASE_DIR, 'static/staticRoot')
STATIC_URL = '/static/'
MEDIA_URL = '/images/'


STATIC_ROOT = os.path.join(BASE_DIR, 'public', 'static/staticRoot') 
MEDIA_ROOT = os.path.join(BASE_DIR, 'public', 'images/') 

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
MEDIA_ROOT =os.path.join(BASE_DIR, "static/images")

DEFAULT_FROM_EMAIL = "support@wiktorw.usermd.net"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "mail26.mydevil.net"
EMAIL_PORT = "587"
EMAIL_HOST_USER = "support@wiktorw.usermd.net"
EMAIL_HOST_PASSWORD = "Naz4d7HEvxRRqvYN"
EMAIL_USE_TLS = True 

CKEDITOR_CONFIGS = {
           'default': {
               'toolbar': 'full',
               'height': 300,
               'width': 800,
           },
       }
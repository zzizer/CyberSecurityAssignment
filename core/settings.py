import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-d^d*dxbox+29i!_bu3hcg5rd5g8-ip9!tvooj*u=ykt6+s!-8u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # other apps
    'EIMS',
    'crispy_forms',
    "crispy_bootstrap5",
    'django_extensions',


    'social_django',
    'defender',
    'easyaudit',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'defender.middleware.FailedLoginMiddleware',
    'easyaudit.middleware.easyaudit.EasyAuditMiddleware',
]

AUTHENTICATION_BACKENDS = (
    # ...
    'social_core.backends.google.GoogleOAuth2',
    # ...
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '866972531477-6f8qp5mvvpjnien87oejb5vhdci4bgis.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'
LOGIN_URL = 'signin'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_URL = 'signout'

ROOT_URLCONF = 'core.urls'

DEFENDER_REDIS_URL = "redis://127.0.0.1:6379/1"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cyber_security',
        'USER': 'postgres',
        'PASSWORD': 'abc123ABC.',
        'PORT': '5432',
    }, 
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

#Static Files
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    BASE_DIR, 'static'
]

MEDIA_URL = '/uploaded_data/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/uploaded_data')

AUTH_USER_MODEL = 'EIMS.NewUser'

# email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'trialassignment3@gmail.com'
EMAIL_HOST_PASSWORD = 'nowfvrrjzkdnxakw'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


DEBUG = True

if DEBUG:
    INSTALLED_APPS += ['sslserver']
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True

    SSL_CERTIFICATE = 'localhost.crt'
    SSL_KEY = 'localhost.key'


SSL_CERTIFICATE = 'localhost.crt'
SSL_KEY = 'localhost.key'

# SESSION_COOKIE_AGE = 10
# SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# SESSION_SAVE_EVERY_REQUEST = True
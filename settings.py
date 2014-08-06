"""
Django settings for shalent project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

#SITE_URL = 'http://localhost:8000' # for testing

SITE_URL = 'http://shalent.com'
FILE_UPLOAD_VIDEO_SIZE = 52428800
FILE_UPLOAD_IMAGE_SIZE = 5428800


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!eqj0u4adqf#!!dxe620-tumg-60ncv^(74m=le_+(a5icf=d%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (
    BASE_DIR + '/Auth/templates/',
    BASE_DIR + '/shalent/templates/'
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "/shalent/static"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth'
)

TEMPLATE_LOADERS = (
    ('pyjade.ext.django.Loader',(
         'django.template.loaders.filesystem.Loader',
         'django.template.loaders.app_directories.Loader',
    )),
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    #'social_auth.backends.facebook.FacebookBackend',
)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Auth',
    'shalent',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'shalent',
        'USER': 'shalent',
        'PASSWORD': 'shalent',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# production api keys
GOOGLE_CLIENT_ID = '375747460177-v3asfjckgb36231jn71ercm1p6kd956r.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'gBh5-qTnBy1L8UGrE9eIbUFJ'

FACEBOOK_APP_ID = '480754732058916'
FACEBOOK_APP_SECRET = 'ba7af5772d1507cca8fe4cd11ae58582'
FACEBOOK_APP_SCOPE = 'email,user_photos,user_videos,user_birthday'

# test api 
#FACEBOOK_APP_ID = '523499947773524'
#FACEBOOK_APP_SECRET = 'cde0f986b5ade4804f50caf0433d55c5'

LOGIN_URL = '/'

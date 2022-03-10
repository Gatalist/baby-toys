from pathlib import Path
import os
from os import environ as env
from dotenv import load_dotenv
load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'ckeditor',
    'ckeditor_uploader',
    'mptt',
    'product',
    'news',
    'users',
    'subscribe',
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

ROOT_URLCONF = 'django_product.urls'

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

                'users.context_processors.getting_basket_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_product.wsgi.application'

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CKEDITOR_UPLOAD_PATH = "uploads/"
# CKEDITOR_BASEPATH = "/assets/ckeditor/ckeditor/"


CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'kama',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 
                        'items': ['Source', '-', 'Save', '-', '-', 'Templates']},
           
            {'name': 'clipboard', 
                        'items': ['Cut', '-', 'Copy', '-', 'Paste', '-', 'PasteText', '-', 'PasteFromWord', '-',
                                  'Undo', '-', 'Redo']},
            
            {'name': 'editing', 
                        'items': ['Find', '-', 'Replace', '-', 'SelectAll']},

            {'name': 'forms',
                        'items': ['Checkbox', '-', 'Radio', '-', 'TextField', '-', 'Textarea', '-', 'Select', '-',
                                  'Button',]},
            '/',
            {'name': 'basicstyles',
                        'items': ['Bold', '-', 'Italic', '-', 'Underline', '-', 'Strike', '-', 'Subscript', '-',
                                  'Superscript', '-', 'RemoveFormat']},

            {'name': 'paragraph',
                        'items': ['NumberedList', '-', 'BulletedList', '-', 'Outdent', '-', 'Indent', '-', 'Blockquote',
                                  '-', 'CreateDiv', '-',
                                  'JustifyLeft', '-', 'JustifyCenter', '-', 'JustifyRight', '-', 'JustifyBlock', '-',
                                  'BidiLtr', '-', 'BidiRtl',]},

            {'name': 'links', 
                        'items': ['Link', '-', 'Unlink',]},

            {'name': 'insert',
                        'items': ['Image', '-', 'Youtube', '-', 'Table', '-', 'HorizontalRule', '-', 'Smiley', '-',
                                  'SpecialChar',]},
            
            {'name': 'styles', 
                        'items': ['Styles', 'Format', 'Font', 'FontSize']},

            {'name': 'colors', 
                        'items': ['TextColor', 'BGColor']},

            {'name': 'tools', 
                        'items': ['ShowBlocks']},
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        'width': '100%',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath',
            'youtube'
        ]),
    }
}


# JSL_DJANGO_SITEMAP_SETTINGS = {"ENABLE": True, "FETCH_URL_FROM": "name", "INCLUDE_APPS": ("ALL",)}


MPTT_ADMIN_LEVEL_INDENT = 20 # отступ меню в админке

ITEM_IN_PAGE = 16

COUNT_DAY = 14
COUNT_LAST_PRODUCT = 8
COUNT_LAST_REVIEW = 8
COUNT_LAST_NEWS = 8

#mail settings
LESYA_EMAIL = env['LESYA_EMAIL']
RECIPIENTS_EMAIL = env['RECIPIENTS_EMAIL']   # кому - почта
DEFAULT_FROM_EMAIL = env['DEFAULT_FROM_EMAIL']  # от кого - почта
EMAIL_BACKEND = env['EMAIL_BACKEND']
EMAIL_HOST = env['EMAIL_HOST']
EMAIL_HOST_USER = env['DEFAULT_FROM_EMAIL']
EMAIL_HOST_PASSWORD = DEFAULT_FROM_EMAIL
EMAIL_PORT = env['EMAIL_PORT']
EMAIL_USE_TLS = env['EMAIL_USE_TLS']


# redis settings
REDIS_HOST = env['REDIS_HOST']
REDIS_PORT = env['REDIS_PORT']


# celery
CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ":" + REDIS_PORT + '/0'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ":" + REDIS_PORT + '/0'
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


try:
    from .local_settings import *
except ImportError:
    from .prod_settings import *

from pathlib import Path
import os
from os import environ as env
from dotenv import load_dotenv
load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

ALLOWED_HOSTS = ["127.0.0.1"]

# Database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'product',
#         'USER': 'user_db',
#         'PASSWORD': 'FLhjrlf35463ty65h',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-o&xj9^rwn&@)7jl+e(lab8z^l$ka0l50@x&%8u)+czlgj(g_zu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'NAME',
#         'USER': 'USER',
#         'PASSWORD': 'PASSWORD',
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

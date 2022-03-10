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
DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", f"{env['SERVER_IP']}", f"{env['SERVER_DNS']}" ]


# Database
DATABASES = {
    'default': {
        'ENGINE': env['DATABASE_ENGINE'],
        'NAME': env['DATABASE_NAME'],
        'USER': env['DATABASE_USER'],
        'PASSWORD': env['DATABASE_PASSWORD'],
        'HOST': env['DATABASE_HOST'],
        'PORT': env['DATABASE_PORT'],
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

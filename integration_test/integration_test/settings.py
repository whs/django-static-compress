import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'secretkey'
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'static_compress',
    'statictest',
]

MIDDLEWARE = []

STATIC_URL = '/static/'

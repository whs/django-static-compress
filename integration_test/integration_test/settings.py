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

# Compress all, no matter file size
STATIC_COMPRESS_MIN_SIZE_KB = 0

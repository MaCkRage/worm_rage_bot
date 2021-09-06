VENDOR_APPS = [
    'drf_yasg',
    'rest_framework',
    'rest_framework.authtoken',
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
]

PROJECT_APPS = [
    'api',
    'user',
    'bot',
    'book',
]

INSTALLED_APPS = (VENDOR_APPS + DJANGO_APPS + PROJECT_APPS)

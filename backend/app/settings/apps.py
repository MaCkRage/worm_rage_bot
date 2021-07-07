VENDOR_APPS = [
    'drf_yasg',
    'rest_framework',
    'rest_framework.authtoken',
    'mptt',
    'bulk_update_or_create',
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
    'products',
]

INSTALLED_APPS = (VENDOR_APPS + DJANGO_APPS + PROJECT_APPS)

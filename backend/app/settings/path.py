import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ROOT_URLCONF = 'app.urls'

WSGI_APPLICATION = 'app.wsgi.application'

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'public', 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'public', 'media')

TEMPLATES_PATH = os.path.join(BASE_DIR, '..', 'frontend', 'templates')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '..', 'frontend', 'src', 'app', 'dist'),
    os.path.join(BASE_DIR, '..', 'frontend', 'src', 'backend_static'),
]

LOGIN_URL = '/'

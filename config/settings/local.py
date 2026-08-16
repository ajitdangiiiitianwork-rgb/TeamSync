from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
import subprocess
import sys

from .base import *

DEBUG = False

f = open(os.path.join(SECRETS_DIR, 'production.json'))
json_object = json.load(f)

ALLOWED_HOSTS += json_object['ALLOWED_HOSTS']

RUNSERVER = 'runserver' in sys.argv
if RUNSERVER:
    DEBUG = True
    ALLOWED_HOSTS = [
        '127.0.0.1',
        'localhost',
    ]


# WSGI
WSGI_APPLICATION = 'config.wsgi.production.application'

INSTALLED_APPS += [
    'storages',
]

# DEFAULT_FILE_STORAGE = 'config.storages.S3DefaultStorage'
# STATICFILES_STORAGE = 'config.storages.S3StaticStorage'

AWS_ACCESS_KEY_ID = json_object['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = json_object['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = json_object['AWS_STORAGE_BUCKET_NAME']
AWS_DEFAULT_ACL = json_object['AWS_DEFAULT_ACL']
AWS_S3_REGION_NAME = json_object['AWS_S3_REGION_NAME']
AWS_S3_SIGNATURE_VERSION = json_object['AWS_S3_SIGNATURE_VERSION']

# DB
DATABASES = json_object['DATABASES']
print(DATABASES)


if os.path.exists('/var/log/django'):
    LOG_DIR = '/var/log/django'
else:
    LOG_DIR = os.path.join(ROOT_DIR, '.log')
    os.makedirs(LOG_DIR, exist_ok=True)

subprocess.call(['chmod', '755', LOG_DIR])

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            'format': '[%(asctime)s] %(message)s',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'file_error': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'django.server',
            'backupCount': 10,
            'filename': os.path.join(LOG_DIR, 'error.log'),
            'maxBytes': 10485760,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file_error'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}

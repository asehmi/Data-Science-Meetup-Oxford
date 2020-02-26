import environ
import os
import sys

from datetime import timedelta

env = environ.Env(
    DEBUG=(bool, False),
    ENVIRONMENT=(str, None),
    ENABLE_FILE_LOGGERS=(bool, False),
    ALLOWED_HOSTS=(list, []),
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'XXXX'
DEBUG = env('DEBUG')
ENVIRONMENT = env('ENVIRONMENT')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')

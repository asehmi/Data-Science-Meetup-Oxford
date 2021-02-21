# django environ
import environ
# system environ
from os import environ as osenv
import os
import sys
from dotenv import load_dotenv, find_dotenv

from datetime import timedelta

# ======== GLOBAL SETTINGS ========

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

USE_AUTHENTICATION = True

# ======== GENERAL ENVIRONMENT VARS ========

env = environ.Env(
    DEBUG=(bool, False),
    ENVIRONMENT=(str, None),
    ENABLE_FILE_LOGGERS=(bool, False),
    ALLOWED_HOSTS=(list, []),
)

DEBUG = env('DEBUG')
ENVIRONMENT = env('ENVIRONMENT')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')

# ======== SECRET ENVIRONMENT VARS ========

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# API General

COMPONENT_BASE_URL = osenv.get('COMPONENT_BASE_URL')
API_BASE_URL = osenv.get('API_BASE_URL')
REMOTE_API_BASE_URL = osenv.get('REMOTE_API_BASE_URL')

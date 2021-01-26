# django environ
import environ
# system environ
from os import environ as osenv
import os
from dotenv import load_dotenv, find_dotenv

# ======== GLOBAL SETTINGS ========

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JOB_SCRIPTS_DIR = os.path.join(BASE_DIR, 'job_scripts')

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

AUTH0_AUTHORITY = osenv.get('AUTH0_AUTHORITY')
AUTH0_DOMAIN = osenv.get('AUTH0_DOMAIN')

# API Client
API_CLIENT_SECRET = osenv.get('API_CLIENT_SECRET')

# Credentials for Airtable
DEFAULT_USERNAME = osenv.get('DEFAULT_USERNAME')
DEFAULT_PASSWORD = osenv.get('DEFAULT_PASSWORD')

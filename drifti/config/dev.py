"""Development config."""
from .base import *  # NOQA
from .core.databases.dev import *
from corsheaders.defaults import default_headers

DEBUG = True

# Security
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "*bQE=R3$#&{(heZ120c9?z1$Fx807HiB-{iiD]^aC5#h$[5,FKN5;MVbh^Npkhr"
)
ALLOWED_HOSTS = [
    ".localhost",
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
]

MIDDLEWARE = [
    "django_tenants.middleware.main.TenantMainMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Enable Cache Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.getenv('REDIS_URL')],
        },
    },
}

# CSRF
CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "http://localhost:5173",
]
CSRF_COOKIE_NAME = 'XSRF-TOKEN'
CSRF_HEADER_NAME = 'HTTP_X_XSRF_TOKEN'

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = list(default_headers) + [
    'x-xsrf-token',
    'access-control-allow-headers',  # this one is important
]

CORS_ALLOW_ALL_ORIGINS = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


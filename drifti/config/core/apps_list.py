BEFORE_DJANGO_APPS = (
    'daphne',
    'django_tenants',
)

DJANGO_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
)

LOCAL_APPS = (
    'apps.customers',
    'apps.users',
)

THIRD_PARTY_APPS = (
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'corsheaders',
    'django_celery_results',
    'django_celery_beat',
    'django_countries',
    'django_filters',
    'import_export',
)

SHARED_APPS = (
    # Django Tenants
    'django_tenants',
    'apps.customers',

    # Management
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'django_celery_results',
    'django_celery_beat',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'import_export'
)

TENANT_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django_celery_results',
    'django_celery_beat',
) + LOCAL_APPS

INSTALLED_APPS = BEFORE_DJANGO_APPS + DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

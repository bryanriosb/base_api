import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_DB_ALIAS = 'default'

DATABASES = {
    DEFAULT_DB_ALIAS: {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT', 5432),
        'CONN_MAX_AGE': 500,
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Database
DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

# Tenant Config
TENANT_MODEL = "customers.Client"
TENANT_DOMAIN_MODEL = "customers.Domain"


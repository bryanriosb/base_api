import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_DB_ALIAS = 'default'
DEFAULT_READ_REPLICA_ALIAS = "replica"

DATABASES = {
    DEFAULT_DB_ALIAS: {
        'DATABASE': DEFAULT_DB_ALIAS,
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT', 5432),
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 500,
    },
    DEFAULT_READ_REPLICA_ALIAS: {
        'DATABASE': DEFAULT_READ_REPLICA_ALIAS,
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST_REPLICA'),
        'PORT': os.getenv('POSTGRES_PORT', 5432),
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 500,
    }
}

DATABASE_ROUTERS = [
    'django_tenants.routers.TenantSyncRouter',
    'drifti.config.core.databases.pro_router.PrimaryReplicaRouter',
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Tenant Config
TENANT_MODEL = "customers.Client"
TENANT_DOMAIN_MODEL = "customers.Domain"


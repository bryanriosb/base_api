# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'tenant_context': {
            '()': 'django_tenants.log.TenantContextFilter'
        },
    },
    'formatters': {
        'tenant_context': {
            'format': '[%(schema_name)s:%(domain_url)s] %(levelname)-7s %(asctime)s %(message)s'
        },
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['tenant_context'],
            'class': 'logging.StreamHandler',
            'formatter': 'tenant_context',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['tenant_context'],
        },

    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console', 'mail_admins'],
            'propagate': True
        },
    }
}
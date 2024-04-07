from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

from tenant_schemas_celery.app import Celery as TenantAwareCelery
from django.conf import settings

app = TenantAwareCelery('drifti')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

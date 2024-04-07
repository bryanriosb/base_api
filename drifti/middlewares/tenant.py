# Django Imports
from django.conf import settings
from django.db import connections

# Django Tenants Imports
from django_tenants.middleware.main import TenantMainMiddleware


DEFAULT_READ_REPLICA_ALIAS = "replica"


class CustomTenantMiddleware(TenantMainMiddleware):
    def process_request(self, request):
        super().process_request(request)
        alias = getattr(settings, DEFAULT_READ_REPLICA_ALIAS, "replica")
        if settings.DATABASES.get(alias):
            self._set_tenant_to_replicas(request, alias)

    def _set_tenant_to_replicas(self, request, alias: str) -> None:
        """
        Function in charge of setting the tenant on the
        read replica alias connection.
        :param request:
        :param alias str:
        :return None:
        """
        connection = connections.__getitem__(alias)
        print('request', request)
        if connection and hasattr(request, "tenant"):
            print('request.tenant', request.tenant)
            connection.set_tenant(request.tenant)


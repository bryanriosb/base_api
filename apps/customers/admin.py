from django.contrib import admin

from django.contrib import admin
from django.contrib.admin.decorators import display
from django_tenants.admin import TenantAdminMixin

from apps.customers.models import Client, Domain


@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'paid_until', 'on_trial', 'is_active', 'created_on')


@admin.register(Domain)
class DomainAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'domain', 'is_primary', 'get_client')

    @display(description='Tenant ID')
    def get_client(self, obj):
        return obj.tenant_id

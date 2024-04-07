from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view()
def health(request):
    return Response("Ok", status=status.HTTP_200_OK)


urlpatterns = [
    # Swagger
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # Django
    path('manager/', admin.site.urls),
    # Health Check
    path('', health, name='health'),
    # Tenants
    path('tenant/', include('apps.customers.urls')),
    path('api/v1/', include(('apps.users.urls', 'users'), namespace='users')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Django
from django.urls import include, path
# Django REST Framework
from rest_framework.routers import DefaultRouter
# Views
from . import views

router = DefaultRouter()
router.register(r'protect_data', views.ProtectDataView, basename='protect_data')
router.register(r'send_email', views.SendEmailView, basename='send_email')


urlpatterns = [
    path('', include(router.urls))
]

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from . import views

router = DefaultRouter()
router.register(r'login', views.SignInView, basename='login')
router.register(r'signup', views.SignUpView, basename='signup')
router.register(r'users', views.ProfileView, basename='users')
router.register(r'otp', views.OTPEmailVerificationView, basename='otp')
router.register(r"groups", views.GroupViewSet, basename='groups')

urlpatterns = [
    path('', include(router.urls)),
]

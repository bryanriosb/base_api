# Django REST
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
# Serializers
from .. import serializers


class ProfileView(viewsets.ModelViewSet):
    serializer_class = serializers.ProfileSerializer
    queryset = serializer_class.Meta.model.objects.filter(available=True).order_by('-created')
    permission_classes = [IsAuthenticated]

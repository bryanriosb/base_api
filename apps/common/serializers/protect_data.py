# Django REST
from rest_framework import serializers


class ProtectDataSerializer(serializers.Serializer):
    text = serializers.CharField()
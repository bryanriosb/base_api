# Django REST
from rest_framework import serializers


class SendEmailSerializer(serializers.Serializer):
    context = serializers.JSONField()
    html = serializers.CharField()
    subject = serializers.CharField()
    to = serializers.ListField()
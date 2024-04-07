from rest_framework import serializers


class SimpleResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()
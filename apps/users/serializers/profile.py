import json
import jwt
from django.utils import timezone
import logging
# Django REST Framework
from rest_framework import serializers

# Models
from ..models import Profile

logger = logging.getLogger(__name__)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        """Meta class."""
        model = Profile
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['profile_id'] = instance.id
        representation['user_id'] = instance.user.id
        representation['username'] = instance.user.username
        representation['first_name'] = instance.user.first_name
        representation['last_name'] = instance.user.last_name
        representation['groups'] = instance.user.groups.values()
        del representation['id']
        del representation['user']
        return representation



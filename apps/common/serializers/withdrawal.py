# Django REST Framework
from rest_framework import serializers

# Models
from ..models import WithdrawalMethod

# Serializers
from django_countries.serializer_fields import CountryField


class WithdrawalMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawalMethod
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'country': {
                'code': instance.country.code,
                'name': instance.country.name
            },
            'type': {
                'id': instance.type.pk,
                'title': instance.type.title
            },

        }


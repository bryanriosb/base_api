
import json
import jwt
from django.utils import timezone
# Django
from django.db.models import Q
from django.contrib.auth import authenticate
# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User, Group
# Utils
from apps.common.utils import OTP
from ..utils.send_otp import send_otp_email


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, min_length=8, max_length=64)
    email = serializers.CharField(required=True)
    role = serializers.CharField(required=True)
    terms_policy = serializers.BooleanField(required=True)

    def validate(self, data):
        """Check if exist username and email."""
        existing_user = User.objects.filter(
            Q(username=data['username']) | Q(email=data['email'])
        ).first()

        if existing_user:
            try:
                profile = existing_user.profile
            except Exception as e:
                raise serializers.ValidationError('The username or email already exists.')

            if (existing_user.username == data['username']) and (existing_user.email == data['email']) \
                    and profile.email_verified:
                raise serializers.ValidationError('The user and email already exist and have been verified.')

            elif (existing_user.username == data['username']) and (existing_user.email == data['email']) \
                    and profile.email_verified is False:

                # Reenvío de codigo de verificación
                send_otp_email(profile)

                error_data = {
                    'error_code': 'otp',
                    'message': 'Existing but unverified email. We will send a new verification code'
                }
                error_payload = json.dumps(error_data)
                raise serializers.ValidationError(error_payload)

            else:
                raise serializers.ValidationError('The username or email already exists.')
        return data


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials.')

        request = self.context['request']
        if request.tenant.schema_name != 'public':
            profile = user.profile
            if not profile.email_verified:
                send_otp_email(profile)
                raise serializers.ValidationError('otp')

        self.context['user'] = user
        return data

    def create(self, data):
        """Generate or retrieve new token."""
        refresh = RefreshToken.for_user(self.context['user'])
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        user = self.context['user']
        user.last_login = timezone.now()
        user.save()
        return user, tokens


class OTPEmailVerificationSerializer(serializers.Serializer):
    """OTP Verification."""
    username = serializers.CharField(required=True)
    otp = serializers.CharField(max_length=6)

    def validate(self, data: dict):
        """OPT code validate."""
        try:
            username = data['username']
            code = data['otp']
            user = User.objects.get(username=username)

            # Get user profile by related_name
            profile = user.profile
            # Verify code
            validated = OTP(profile).verify(code)
            if validated:
                tokens = None
                self.context['profile'] = profile
                return data
            else:
                raise serializers.ValidationError('Invalid or expired OTP code.')
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError("Can't validate OTP code.")

    def save(self):
        """Update is_verified field on profile."""
        profile = self.context['profile']
        if profile.is_verified:
            raise serializers.ValidationError({
                'message': 'The user is already verified.'
            })
        profile.is_verified = True
        profile.save()


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']



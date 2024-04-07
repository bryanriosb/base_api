import pyotp
import logging
from django.contrib.auth.models import User, Group
# Django REST
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.validators import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
# Serializers
from .. import serializers
# Utils
from ...common.utils import ProtectData
from ..utils.send_otp import send_otp_email

logger = logging.getLogger(__name__)


class SignUpView(viewsets.ViewSet):
    serializer_class = serializers.SignUpSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            user_data = {
                'username': request.data['username'],
                'email': request.data['email'],
            }
            user = User.objects.create(**user_data)
            user.set_password(request.data['password'])
            user.save()

            # Protect key OTP verification assigned to each user.
            # This is stored in a database binary field.
            encrypted_o_key = ProtectData(data=pyotp.random_base32()).encrypt()
            instance = serializers.ProfileSerializer.Meta.model
            profile = instance.objects.create(
                user=user,
                role=request.data['role'],
                o_key=encrypted_o_key,
                terms_policy=request.data['terms_policy']
            )

            email_sent = send_otp_email(profile)
            user_data['role'] = request.data['role']

            if email_sent:
                profile.save()
                return Response(
                    {
                        'success': True,
                        'user': user_data,
                        'message': 'We have sent a code to the email for email validation.'
                    }, status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {
                        'success': False,
                        'message': "Couldn't send validation email."
                    }, status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f'Cannot add  user: {e}')
            response = {
                'success': False,
                'message': 'Cannot user create.'
            }
            detail = e.__dict__.get('detail')
            if detail.get('non_field_errors'):
                error = detail.get('non_field_errors')
                parse = error[0]
                if error[0] == 'otp':
                    response['otp_error'] = True
                    response['message'] = ('Correo existente pero no verificado. Enviaremos un nuevo código de '
                                           'verificación.')
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class OTPEmailVerificationView(viewsets.ViewSet):
    """Email verification."""
    serializer_class = serializers.OTPEmailVerificationSerializer

    def create(self, request, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                response = {
                    'success': True,
                    'message': 'Activación de cuenta exitosa.'
                }
                user_payload = serializer.validated_data
                if user_payload.get('tokens'):
                    response['payload'] = user_payload
                return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"OTP Verify Error: {e}")
            return Response(
                {
                    'success': False,
                    'message': 'No se pudo verificar el código'
                }, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def resend(self, request):
        username = request.data['username']
        profile = User.objects.get(username=username).profile
        if profile.email_verified:
            return Response(
                {
                    'success': False,
                    'message': 'El usuario ya ha sido verificado.'
                }, status=status.HTTP_400_BAD_REQUEST
            )
        if profile:
            send_otp_email(profile)
            return Response(
                {
                    'success': True,
                    'message': 'Un nuevo código fue enviado al correo.'
                }, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'success': False,
                    'message': 'No fue posible enviar un nuevo código.'
                }, status=status.HTTP_400_BAD_REQUEST
            )


class SignInView(viewsets.ViewSet):
    """Create access tokens and return user profile data."""
    serializer_class = serializers.SignInSerializer
    http_method_names = ['post']

    def create(self, request, **kwargs):
        profile = None
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            user, tokens = serializer.save()
            user_payload = None

            # Get user profile from role
            response = {
                'success': True,
                'tokens': tokens,
                'message': f'Bienvenido {user.username}'
            }
            if request.tenant.schema_name != 'public':
                profile = user.profile
                profile_payload = serializers.ProfileSerializer(profile).data
                response['user'] = profile_payload

            return Response(response, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.error(f'Login error: {e.detail}')
            error = None
            response = {
                    'success': False,
                    'message': error if error else 'No fue posible iniciar sesión'
            }
            if e.__dict__.get('detail'):
                detail = e.__dict__.get('detail')
                if detail.get('password'):
                    error = detail.get('password')
                    response['message'] = error
                elif detail.get('non_field_errors'):
                    error = detail.get('non_field_errors')
                    response['message'] = error
                    if error[0] == 'otp':
                        response['otp_error'] = True
                        response['message'] = ('Correo existente pero no verificado. Enviaremos un nuevo código de '
                                               'verificación.')
            elif e.detail:
                error = e.detail
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = [IsAuthenticated]
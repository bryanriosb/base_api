# Utils
import base64
import json
from ..utils import ProtectData

# Django REST
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

# Serializers
from ..serializers import ProtectDataSerializer


class ProtectDataView(viewsets.ViewSet):
    """Encrypt access tokens to share with unity using AES key.
    This method get a base64 by POST request."""
    serializer_class = ProtectDataSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        access_base64 = request.data['text']
        data = base64.b64decode(access_base64).decode('latin-1').encode('utf-8').decode()

        encrypted = ProtectData(data=data).aes_encrypt()

        try:
            # Verify if token is valid.
            decrypted = ProtectData(encrypted_data=encrypted).aes_decrypt()
            decrypted_payload = json.loads(decrypted)

            if decrypted_payload['created']:
                return Response(
                    {
                        'success': True,
                        'payload': encrypted
                    }, status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {
                    'success': False,
                    'message': 'There were problems creating the login.'
                }, status=status.HTTP_409_CONFLICT
            )

    @action(methods=['POST'], detail=False)
    def aes_decrypt(self, request, *args, **kwargs):
        encrypted = request.data['text']
        decrypted = ProtectData(encrypted_data=encrypted).aes_decrypt()

        return Response(
            {
                'success': True,
                'payload': decrypted
            }, status=status.HTTP_200_OK
        )
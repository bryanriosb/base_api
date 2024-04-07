# Django REST
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from apps.common.serializers.send_email import SendEmailSerializer
from apps.common.utils import Email


class SendEmailView(viewsets.ViewSet):
    serializer_class = SendEmailSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def create(self, request):
        try:
            email_payload = request.data
            Email().send(email_payload)

            return Response(
                {
                    'success': True,
                    'message': 'Email Sent.'
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print('error', e)
            return Response(
                {
                    'success': False,
                    'message': 'Cannot Email Sent.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

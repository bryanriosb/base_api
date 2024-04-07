from channels.db import database_sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication


class WebSocketAuth:
    @database_sync_to_async
    def authenticate(self, token):
        jwt_object = JWTAuthentication()
        validated_token = jwt_object.get_validated_token(token)
        user = jwt_object.get_user(validated_token)
        return user


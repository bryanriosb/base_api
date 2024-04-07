from channels.db import database_sync_to_async
from django.db import close_old_connections
from django_tenants.utils import schema_context
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from channels.middleware import BaseMiddleware
from urllib.parse import parse_qs
from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.security.websocket import WebsocketDenier


class JwtAuthMiddleware(BaseMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.app = app

    @database_sync_to_async
    def get_user(self, token):
        jwt_object = JWTAuthentication()
        validated_token = jwt_object.get_validated_token(token)
        user = jwt_object.get_user(validated_token)
        return user

    async def __call__(self, scope, receive, send):
        params = parse_qs(scope["query_string"].decode())
        token = params["token"][0]
        # Close old database connections to prevent usage of timed out connections
        close_old_connections()
        # Try to authenticate the user
        try:
            # with schema_context('public'):
            # This will automatically validate the token and raise an error if token is invalid
            user = await self.get_user(token)
            if user is None:
                raise ValueError("Invalid token")
            scope['user'] = user
            return await self.app(scope, receive, send)
        except (InvalidToken, TokenError) as e:
            denier = WebsocketDenier()
            return await denier(scope, receive, send)
            # raise ValueError("Invalid token")


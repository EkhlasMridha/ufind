import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
from user.models import User


class JWTAuhtentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)

        if not auth_data:
            return None

        prefix, token = auth_data.decode('utf-8').split(' ')

        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET, algorithms='HS256')

            user = User.objects.get(email=payload['email'])
            return (user, token)
        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed("Invalid token")
        except jwt.ExpiredSignatureError as identifier:
            raise exceptions.AuthenticationFailed("Expired token")

        return super().authenticate(request)


from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import Token
from django.conf import settings
class JWTCookieAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token=dict(request.COOKIES).get(settings.SIMPLE_JWT["ACCESS_TOKEN_NAME"],None)
        if raw_token is None:
            return None
        validated_token=self.get_validated_token(raw_token)
        return self.get_user(validated_token),validated_token

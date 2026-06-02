from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.models import User

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        
        if header is None:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token

    def get_user(self, validated_token):
        try:
            user_id = validated_token.get('user_id')
            return User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            from rest_framework_simplejwt.exceptions import InvalidToken
            raise InvalidToken('User not found.')
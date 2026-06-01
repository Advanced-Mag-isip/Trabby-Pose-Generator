from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom authentication class that extends SimpleJWT to read 
    tokens from secure HTTP-only cookies instead of headers.
    """
    def authenticate(self, request):
        header = self.get_header(request)
        
        if header is None:
            # Fallback to reading from cookies if the header isn't present
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
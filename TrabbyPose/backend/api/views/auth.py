from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
import hashlib

from api.models import User
from api.auth_serializers import (
    UserLoginSerializer,
    UserSerializer,
    UserProfileSerializer
)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Logs in a user and attaches JWT tokens via secure, HttpOnly cookies.
    """

    serializer = UserLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        user.updated_at = timezone.now()
        user.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        # Omit raw tokens from the frontend payload body for XSS safety
        response = Response(
            {
                'message': 'Login successful.',
                'user': UserSerializer(user).data,
            },
            status=status.HTTP_200_OK
        )
        
        # Set Access Cookie
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=access_token,
            expires=timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            path='/'
        )
        
        # Set Refresh Cookie
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value=refresh_token,
            expires=timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            path='/'
        )
        
        return response
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny]) # Changed to AllowAny so users with expired access tokens can still log out
def logout_user(request):
    """
    Logs out the user by blacklisting their refresh token and deleting local auth cookies.
    """
    response = Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)
    
    # Extract the refresh token from cookies to blacklist it safely on the server side
    refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except (TokenError, AttributeError):
            pass # Token is already invalid or blacklisting configuration is absent
            
    # Instruct client browser to instantly drop auth cookies
    response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE'], path='/')
    response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'], path='/')
    
    return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """
    Retrieves the authenticated user instance determined by the CookieJWTAuthentication class.
    """
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    """
    Rotates and issues a fresh access token using the stored refresh cookie.
    """
    refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
    
    if not refresh_token:
        return Response({'error': 'Refresh token missing.'}, status=status.HTTP_401_UNAUTHORIZED)
        
    try:
        refresh = RefreshToken(refresh_token)
        new_access_token = str(refresh.access_token)
        
        response = Response({'message': 'Token refreshed successfully.'}, status=status.HTTP_200_OK)
        
        # Apply fresh updated access token to cookie
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=new_access_token,
            expires=timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            path='/'
        )
        
        # If ROTATE_REFRESH_TOKENS is enabled, update the refresh cookie too
        if settings.SIMPLE_JWT.get('ROTATE_REFRESH_TOKENS', False):
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                value=str(refresh),
                expires=timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                path='/'
            )
            
        return response
        
    except TokenError:
        return Response({'error': 'Token is invalid or expired.'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')

    if not current_password or not new_password:
        return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Verify current password
    hashed_current = hashlib.sha256(current_password.encode()).hexdigest()
    if user.password != hashed_current:
        return Response({'error': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

    # Save new password
    user.password = hashlib.sha256(new_password.encode()).hexdigest()
    user.save()

    return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
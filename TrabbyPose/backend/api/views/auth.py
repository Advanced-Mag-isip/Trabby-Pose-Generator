"""
Authentication Views for user login and profile management.

Provides API endpoints for:
- User login with JWT token generation
- User logout
- Get current user profile
- Refresh JWT tokens

Note: User management is handled through Django admin panel.
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

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
    Login a user and return JWT tokens.
    
    Expected POST data:
    {
        "user_name": "username",
        "password": "password"
    }
    
    Returns:
    - 200: Login successful with tokens and user data
    - 400: Invalid credentials or validation errors
    """
    serializer = UserLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        user.updated_at = timezone.now()
        user.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response(
            {
                'message': 'Login successful.',
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            },
            status=status.HTTP_200_OK
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """
    Logout a user.
    
    Simply invalidates the token on the client side. The token will still be valid
    until expiration. For complete token blacklisting, implement a token blacklist
    using the drf-simplejwt TokenBlacklist feature.
    
    Returns:
    - 200: Logout successful
    """
    return Response(
        {'message': 'Logout successful. Please remove the token from client storage.'},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """
    Get the current authenticated user's profile.
    
    Requires: Valid JWT token in Authorization header
    
    Returns:
    - 200: Current user profile
    - 401: Unauthorized
    """
    try:
        # Get the user from the JWT token
        user = User.objects.get(user_id=request.auth.get('user_id') if hasattr(request.auth, 'get') else None)
    except (User.DoesNotExist, TypeError, AttributeError):
        # Fallback: Try to find user by checking if request has user info
        # This is a fallback for token-based auth
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = UserProfileSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """
    Get the current authenticated user's information.
    
    This endpoint works with JWT tokens to retrieve the user making the request.
    
    Requires: Valid JWT token in Authorization header
    
    Returns:
    - 200: Current user information
    - 401: Unauthorized
    """
    # The JWT token contains the user_id, we need to retrieve it
    # Django REST Framework's TokenAuthentication doesn't include user_id in token by default
    # We need to extract it from the request.user object
    
    if request.user and request.user.is_authenticated:
        # If using session auth, request.user will be the User object
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(
        {'error': 'Not authenticated'},
        status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    """
    Refresh JWT access token.
    
    Expected POST data:
    {
        "refresh": "refresh_token_string"
    }
    
    Returns:
    - 200: New access token
    - 400: Invalid refresh token
    """
    from rest_framework_simplejwt.views import TokenRefreshView
    
    view = TokenRefreshView.as_view()
    return view(request)

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from api.models import User
from api.serializers_auth import (
    UserLoginSerializer,
    UserSerializer,
    UserCreateSerializer,
    UserProfileSerializer,
    UserListSerializer,
)


def get_authenticated_user(request):
    """Helper function to get authenticated user from session"""
    user_id = request.session.get('user_id')
    if user_id:
        try:
            return User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return None
    return None


def require_auth(view_func):
    """Decorator to require authentication"""
    def wrapper(request, *args, **kwargs):
        user = get_authenticated_user(request)
        if not user:
            return Response(
                {'error': 'Authentication required. Please log in first.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        request.auth_user = user
        return view_func(request, *args, **kwargs)
    return wrapper


def require_admin(view_func):
    """Decorator to require admin authentication"""
    def wrapper(request, *args, **kwargs):
        user = get_authenticated_user(request)
        if not user:
            return Response(
                {'error': 'Authentication required. Please log in first.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if not user.is_admin:
            return Response(
                {'error': 'Admin privileges required.'},
                status=status.HTTP_403_FORBIDDEN
            )
        request.auth_user = user
        return view_func(request, *args, **kwargs)
    return wrapper


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    User login endpoint
    
    Expected POST data:
    {
        "user_name": "string",
        "password": "string"
    }
    
    Returns: {
        "user": {...},
        "message": "Login successful"
    }
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        # Store user ID in session
        request.session['user_id'] = user.user_id
        request.session['is_admin'] = user.is_admin
        return Response({
            'user': UserSerializer(user).data,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request):
    """
    User logout endpoint
    
    Clears the session for the current user
    """
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'is_admin' in request.session:
        del request.session['is_admin']
    
    return Response({
        'message': 'Logout successful'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_current_user(request):
    """
    Get current authenticated user profile
    
    Returns: {
        "user": {...}
    }
    """
    user = get_authenticated_user(request)
    if not user:
        return Response(
            {'error': 'Not authenticated'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    return Response({
        'user': UserProfileSerializer(user).data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    """
    Create a new user account (admin only after first user)
    
    Expected POST data:
    {
        "first_name": "string",
        "last_name": "string",
        "user_name": "string",
        "email_address": "string",
        "password": "string",
        "confirm_password": "string",
        "is_permitted": 1 or 0
    }
    
    Admin must be logged in and have admin privileges.
    For initial setup, allow creation without auth. After first admin is created,
    this should be restricted to admin-only.
    """
    # Check if this is the first user (admin seeding)
    user_count = User.objects.count()
    
    if user_count > 0:
        # Not the first user, check if requester is admin
        admin = get_authenticated_user(request)
        if not admin or not admin.is_admin:
            return Response(
                {'error': 'You do not have permission to create users. Only admins can create users.'},
                status=status.HTTP_403_FORBIDDEN
            )
    
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # If this is the first user, make them admin
        if user_count == 0:
            user.is_admin = True
        
        user.created_at = timezone.now()
        user.updated_at = timezone.now()
        user.save()
        
        return Response({
            'user': UserSerializer(user).data,
            'message': 'User created successfully'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_users(request):
    """
    List all users in the system (admin only)
    
    Returns: {
        "users": [...]
    }
    """
    admin = get_authenticated_user(request)
    
    if not admin or not admin.is_admin:
        return Response(
            {'error': 'You do not have permission to view users. Only admins can view user list.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    users = User.objects.all().order_by('created_at')
    serializer = UserListSerializer(users, many=True)
    
    return Response({
        'users': serializer.data,
        'count': users.count()
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_user(request, user_id):
    """
    Delete a user account (admin only)
    
    URL parameter: user_id
    """
    admin = get_authenticated_user(request)
    
    if not admin or not admin.is_admin:
        return Response(
            {'error': 'You do not have permission to delete users.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Prevent deleting the last admin
    if user.is_admin:
        admin_count = User.objects.filter(is_admin=True).count()
        if admin_count <= 1:
            return Response(
                {'error': 'Cannot delete the last admin user.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    user_name = user.user_name
    user.delete()
    
    return Response({
        'message': f'User {user_name} deleted successfully'
    }, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
@permission_classes([AllowAny])
def update_user(request, user_id):
    """
    Update user details (users can update their own, admins can update any)
    
    URL parameter: user_id
    
    Expected data (any combination):
    {
        "first_name": "string",
        "last_name": "string",
        "email_address": "string",
        "is_permitted": 1 or 0
    }
    """
    auth_user = get_authenticated_user(request)
    
    if not auth_user:
        return Response(
            {'error': 'Not authenticated'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Users can only update their own profile, admins can update anyone
    if user.user_id != auth_user.user_id and not auth_user.is_admin:
        return Response(
            {'error': 'You can only update your own profile.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Allow partial updates
    allowed_fields = ['first_name', 'last_name', 'email_address', 'is_permitted']
    
    for field in allowed_fields:
        if field in request.data:
            setattr(user, field, request.data[field])
    
    user.updated_at = timezone.now()
    user.save()
    
    return Response({
        'user': UserSerializer(user).data,
        'message': 'User updated successfully'
    }, status=status.HTTP_200_OK)


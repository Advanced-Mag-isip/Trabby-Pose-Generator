"""
Authentication Serializers for user login and profile management.

Handles serialization of user credentials and token operations.
"""

from rest_framework import serializers
from api.models import User
import hashlib


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    
    Authenticates user credentials and returns user info.
    """
    user_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        """Validate login credentials."""
        user_name = attrs.get('user_name')
        password = attrs.get('password')
        
        try:
            user = User.objects.get(user_name=user_name)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid username or password.')
        
        # Hash the provided password and compare
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if user.password != hashed_password:
            raise serializers.ValidationError('Invalid username or password.')
        
        # Check if user is permitted
        if user.is_permitted == 0:
            raise serializers.ValidationError('User account is not permitted.')
        
        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user data.
    
    Returns user information without sensitive data.
    """
    class Meta:
        model = User
        fields = ['user_id', 'user_name', 'email_address', 'first_name', 'last_name', 'is_permitted', 'created_at']
        read_only_fields = ['user_id', 'created_at']


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile information.
    
    Used for fetching current user profile.
    """
    class Meta:
        model = User
        fields = ['user_id', 'user_name', 'email_address', 'first_name', 'last_name', 'is_permitted']
        read_only_fields = fields


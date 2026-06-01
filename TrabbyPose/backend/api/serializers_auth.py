from rest_framework import serializers
from django.contrib.auth.hashers import check_password, make_password
from api.models import User


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    user_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user_name = data.get('user_name')
        password = data.get('password')

        try:
            user = User.objects.get(user_name=user_name)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password.")

        # Check password
        if not check_password(password, user.password):
            raise serializers.ValidationError("Invalid username or password.")

        # Check if user is permitted to log in
        if user.is_permitted == 0:
            raise serializers.ValidationError("Your account is not active. Please contact an administrator.")

        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'user_name',
            'email_address',
            'is_permitted',
            'is_admin',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['user_id', 'created_at', 'updated_at', 'is_admin']


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new users (admin only)"""
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'user_name',
            'email_address',
            'password',
            'confirm_password',
            'is_permitted',
        ]

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        # Check if username already exists
        if User.objects.filter(user_name=data['user_name']).exists():
            raise serializers.ValidationError({"user_name": "This username is already taken."})

        # Check if email already exists
        if User.objects.filter(email_address=data['email_address']).exists():
            raise serializers.ValidationError({"email_address": "This email is already registered."})

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile (read-only for logged-in user)"""
    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'user_name',
            'email_address',
            'is_permitted',
            'is_admin',
            'created_at',
            'updated_at',
        ]
        read_only_fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
    """Serializer for listing users (admin only)"""
    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'user_name',
            'email_address',
            'is_permitted',
            'is_admin',
            'created_at',
        ]
        read_only_fields = '__all__'

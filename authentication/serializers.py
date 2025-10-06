import re
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate


# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate(self, data):
        # Check for password requirements (optional)
        password = data.get('password')
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r"\d", password):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not re.search(r"[A-Z]", password):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


# Login serializer 
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        
        if not user.is_active:
            raise serializers.ValidationError("Account is not active.")
        
        return data

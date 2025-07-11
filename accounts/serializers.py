from rest_framework import serializers
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    # We add password as a write_only field, so it's used for creation
    # but is never sent back in a response.
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        # These are the fields the frontend will send
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'role')

    def create(self, validated_data):
        # This create method is called when we save the serializer.
        # It uses Django's create_user method which correctly
        # hashes the password.
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data['role']
        )
        return user
    
# Add this class to accounts/serializers.py

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # These are the "safe" fields we will send back to the frontend
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role')
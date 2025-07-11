from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer # Add UserProfileSerializer
# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer
from .models import CustomUser

class UserRegistrationView(generics.CreateAPIView):
    """
    An endpoint for creating a new user.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    # We set permission_classes to AllowAny so that unauthenticated
    # users can access this endpoint to register.
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role
            },
            "message": "User created successfully.",
        }, status=status.HTTP_201_CREATED)
        
# Add this class to accounts/views.py

class UserProfileView(generics.RetrieveAPIView):
    """
    An endpoint to get the profile of the currently logged-in user.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    # This is the magic line! It tells DRF to ensure the user is
    # authenticated with a valid token before allowing access to this view.
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # This method overrides the default behavior to simply return
        # the user associated with the request's token.
        return self.request.user
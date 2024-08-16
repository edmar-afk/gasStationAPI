# views.py
from rest_framework import generics, permissions, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import UserSerializer, ProfileSerializer, GasolineSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Profile, Gasoline
from rest_framework.views import APIView
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework.decorators import api_view


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # Extract user data
        user_data = self.request.data

        # Check for existing username
        username = user_data.get('username')
        email = user_data.get('email')

        if User.objects.filter(username=username).exists():
            raise ValidationError({'username': 'A user with this username already exists.'})
        
        if User.objects.filter(email=email).exists():
            raise ValidationError({'email': 'A user with this email already exists.'})
        
        # Save the user and profile
        user = serializer.save()
        
        # Optionally, you can handle additional logic here if needed

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    
class ProfileDetailView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        try:
            profile = Profile.objects.get(user__id=user_id)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        

class GasolineCreateView(generics.CreateAPIView):
    queryset = Gasoline.objects.all()
    serializer_class = GasolineSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print(f"Creating gasoline with data: {self.request.data}")
        serializer.save(station=self.request.user)
        
class GasolineListView(generics.ListAPIView):
    serializer_class = GasolineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter gasoline entries by the logged-in user
        return Gasoline.objects.filter(station=self.request.user)
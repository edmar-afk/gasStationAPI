# views.py
from rest_framework import generics, permissions, views, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import UserSerializer, ProfileSerializer, GasolineSerializer, ActivePromoSerializer, UserSearchSerializer, UpdateUserSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Profile, Gasoline, ActivePromo
from rest_framework.views import APIView
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework.decorators import api_view
from django.db.models import Q


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
    
class ActivePromoCreateView(generics.CreateAPIView):
    queryset = ActivePromo.objects.all()
    serializer_class = ActivePromoSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # Set the station field to the current user
        serializer.save(station=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = ActivePromoSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserPromosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        promos = ActivePromo.objects.filter(station=user)
        serializer = ActivePromoSerializer(promos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ActivePromoDeleteView(generics.DestroyAPIView):
    queryset = ActivePromo.objects.all()
    serializer_class = ActivePromoSerializer

    def delete(self, request, *args, **kwargs):
        promo_id = kwargs.get('pk')
        try:
            promo = ActivePromo.objects.get(pk=promo_id)
            self.perform_destroy(promo)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ActivePromo.DoesNotExist:
            return Response({'detail': 'Promo not found.'}, status=status.HTTP_404_NOT_FOUND)
        


class UserListByLastNameView(APIView):
    serializer_class = UserSearchSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        last_name = self.kwargs['last_name']
        return User.objects.filter(last_name__icontains=last_name).prefetch_related('gasoline_set')

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GasolineDeleteAPIView(generics.DestroyAPIView):
    queryset = Gasoline.objects.all()
    serializer_class = GasolineSerializer
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        gasoline_id = kwargs.get('id')
        try:
            gasoline = self.get_object()
            gasoline.delete()
            return Response({"detail": "Gasoline deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Gasoline.DoesNotExist:
            return Response({"detail": "Gasoline not found."}, status=status.HTTP_404_NOT_FOUND)


class GasolineUpdateAPIView(APIView):
    def put(self, request, id, format=None):
        try:
            gasoline = Gasoline.objects.get(id=id)
        except Gasoline.DoesNotExist:
            return Response({'error': 'Gasoline not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = GasolineSerializer(gasoline, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GasolineDetailView(generics.RetrieveAPIView):
    queryset = Gasoline.objects.all()  # The queryset to be used for retrieving a single object
    serializer_class = GasolineSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'  # Field to look up the object
    
class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = UpdateUserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
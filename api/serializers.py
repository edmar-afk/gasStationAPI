from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, GasStation, Images, ActivePromo



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['business_permit']  # Removed 'user' as it's not needed in the input

class UserSerializer(serializers.ModelSerializer):
    business_permit = serializers.FileField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'email', 'password', 'business_permit']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        business_permit = validated_data.pop('business_permit')
        user = User.objects.create_user(**validated_data)
        # Create Profile for the user
        Profile.objects.create(user=user, business_permit=business_permit)
        return user
        
        
class GasStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GasStation
        fields = ['owner', 'station_name', 'address', 'description', 'price']

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['station', 'imges']

class ActivePromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivePromo
        fields = ['station', 'discount', 'expired_at']

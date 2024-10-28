from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, GasStation, Images, ActivePromo, Gasoline


class UserSerializer(serializers.ModelSerializer):
    business_permit = serializers.FileField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'email', 'last_name', 'password', 'business_permit']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        business_permit = validated_data.pop('business_permit')
        user = User.objects.create_user(**validated_data)
        # Create Profile for the user
        Profile.objects.create(user=user, business_permit=business_permit)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'bio', 'business_permit', 'profile_pic']   
        
class GasStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GasStation
        fields = ['station_name', 'address', 'description', 'price']
        
class ImagesSerializer(serializers.ModelSerializer):
    station = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Images
        fields = ['station', 'imges']


class ActivePromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivePromo
        fields = ['id', 'title', 'description']

class GasolineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gasoline
        fields = ['id', 'type', 'price']
        
class UserSearchSerializer(serializers.ModelSerializer):
    gasoline_entries = GasolineSerializer(source='gasoline_set', many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'email', 'last_name', 'gasoline_entries']
        
        
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
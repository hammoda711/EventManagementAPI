from rest_framework import serializers
from django.contrib.auth import get_user_model
from events.serializers import EventSerializer
from accounts.models import HostProfile

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # Ensure password is write-only
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user



class UserProfileSerializer(serializers.ModelSerializer):
    events_attending = EventSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name','image','events_attending']
        read_only_fields = ['id']  
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},       # Ensure email is always required
        }

    def update(self, instance, validated_data):
        # Update profile fields
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.image = validated_data.get('image', instance.image)

        # If password is provided, hash it
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()
        return instance


class HostProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    events_hosted = EventSerializer(many=True, read_only=True,)
    class Meta:
        model = HostProfile
        fields = ['organization','username','events_hosted']
        read_only_fields = ['username']  # Ensure user cannot be modified

    def create(self, validated_data):
        # Create a new HostProfile for the user
        # Get the logged-in user
        request_user = self.context['request'].user  
        # Check if the user already has a host profile
        if HostProfile.objects.filter(user=request_user).exists():
            raise serializers.ValidationError("Host profile already exists.")
            
        return HostProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Update the host profile information
        instance.organization = validated_data.get('organization', instance.organization)
        instance.save()
        return instance
    


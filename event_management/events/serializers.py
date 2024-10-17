from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Event

User = get_user_model()



class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class EventSerializer(serializers.ModelSerializer):
    #attendees = UserProfileSerializer(many=True, read_only=True)
    host = serializers.CharField(source='host.user.username', read_only=True)
    attendees = AttendeeSerializer(many=True, read_only=True)
    date_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=True)
    created_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date_time', 'location', 'host', 'capacity', 'created_date','attendees']
        read_only_fields = ['id', 'created_date','attendees']

    def validate_date_time(self, value):
        # Ensure the event is scheduled in the future
        if value < timezone.now():
            raise serializers.ValidationError("Event cannot be scheduled in the past.")
        return value

    def validate_capacity(self, value):
        # Ensure capacity is a positive integer
        if value <= 0:
            raise serializers.ValidationError("Event capacity must be a positive number.")
        return value
    
    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value


from datetime import timezone
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
    attendees = AttendeeSerializer(many=True, read_only=True)  # Use AttendeeSerializer for attendees

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date_time', 'location', 'host', 'capacity', 'created_date','attendees']
        read_only_fields = ['id', 'created_date','attendees']

    def validate_date_time(self, value):
        # Ensure the event is scheduled in the future
        if value < timezone.now():
            raise serializers.ValidationError("Event cannot be scheduled in the past.")
        return value

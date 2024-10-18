from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from events.models import Event
from events.pagination import CustomPagination
from events.serializers import EventSerializer
from accounts.permissions import IsEventHost, IsSuperUser, IsSuperUserOrHost, IsOwner
from django.utils import timezone
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError, PermissionDenied

class EventRegistrationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        event_id = self.kwargs.get('event_id')
        event = get_object_or_404(Event, id=event_id)

        # Check if the user is already registered for the event
        if request.user in event.attendees.all():
            return Response({"message": "You are already registered for this meeting."}, status=status.HTTP_400_BAD_REQUEST)

        if event.capacity > 0:
            event.attendees.add(request.user)
            event.decrease_capacity()
            return Response({"message": "Successfully registered for the event."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "The event is full."}, status=status.HTTP_400_BAD_REQUEST)



class CreateEventView(generics.CreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrHost]

    def perform_create(self, serializer):
         # Automatically set the host to the currently logged-in user 
        host_profile = self.request.user.hostprofile
        if not host_profile:
            raise ValidationError("You must have a host profile to create an event.")
        serializer.save(host=host_profile)
       


class DeleteEventView(generics.DestroyAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsEventHost | IsSuperUser ]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Event.objects.all()  # Superusers can delete any event
        return Event.objects.filter(host__user=user)
    



class UpdateRetrieveEventView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update an event only if the user is the host of the event.
    """
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsEventHost ]  # Ensure the user is authenticated and is a host

    def get_queryset(self):
        # Get all events hosted by the user
        user = self.request.user
        return Event.objects.filter(host__user=user)
    #we may need perform_update for notification


class UserUpcomingEventsView(generics.ListAPIView):
    """
    List all upcoming events for attendees.
    """
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields = ['title', 'location']
    search_fields = ['title', 'location']
    pagination_class = CustomPagination

    def get_queryset(self):
        # Get the user from the request
        user = self.request.user
        # Return upcoming events that the user is attending
        return Event.objects.filter(attendees=user, date_time__gt=timezone.now()).order_by('-created_date')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Modify the response to exclude 'attendees'
        response_data = serializer.data
        for event in response_data:
            event.pop('attendees', None)  # Remove the attendees field if it exists

        return Response(response_data)

class HostsUpcomingEventsView(generics.ListAPIView):
    """
    List all upcoming events for hosts.
    """
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields = ['title', 'location']
    search_fields = ['title', 'location']
    pagination_class = CustomPagination

    def get_queryset(self):
        # Get the user from the request
        user = self.request.user
        if not hasattr(user, 'hostprofile'):
            raise PermissionDenied("You are not a host and cannot access this view.")
        # Return all upcoming events hosted by the user
        return Event.objects.filter(host__user=user, date_time__gt=timezone.now()).order_by('-created_date')
    


class EventsListView(generics.ListAPIView):
    queryset = Event.objects.all().order_by('-created_date')
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsSuperUser]
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields = ['title', 'location']
    search_fields = ['title', 'location']
    pagination_class = CustomPagination

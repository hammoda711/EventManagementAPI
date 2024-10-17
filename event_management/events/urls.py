from django.urls import path
from events.views import CreateEventView, DeleteEventView, EventRegistrationView, EventsListView, HostsUpcomingEventsView, UpdateRetrieveEventView, UserUpcomingEventsView

urlpatterns = [
    path('create/', CreateEventView.as_view(), name='create-event'),
    path('<int:pk>/delete/', DeleteEventView.as_view(), name='delete-event'),
    path('<int:pk>/detail/', UpdateRetrieveEventView.as_view(), name='event-detail'),
    path('upcoming/user/', UserUpcomingEventsView.as_view(), name='user-upcoming-events'),
    path('upcoming/host/', HostsUpcomingEventsView.as_view(), name='host-upcoming-events'),
    path('all/', EventsListView.as_view(), name='events-list'),
    path('<int:event_id>/attend/', EventRegistrationView.as_view(), name='attend-event'),
]
from django.urls import path
from events.views import CreateEventView, DeleteEventView

urlpatterns = [
    path('events/create/', CreateEventView.as_view(), name='create-event'),
    path('events/delete/<int:pk>/', DeleteEventView.as_view(), name='delete-event'),

]
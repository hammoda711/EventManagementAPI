from datetime import timezone
from django.db import models

from accounts.models import HostProfile

# Create your models here.
class Event(models.Model):
    host = models.ForeignKey('accounts.HostProfile', on_delete=models.CASCADE, related_name='event_host') #will be used in source in the host serializer
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(HostProfile, on_delete=models.CASCADE, related_name='events')
    capacity = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} hosted by {self.host}"
    

    def save(self, *args, **kwargs):
        # Ensure the event is not scheduled in the past
        if self.date_time < timezone.now():
            raise ValueError("Event cannot be scheduled in the past.")
        super(Event, self).save(*args, **kwargs)

    def decrease_capacity(self):
        # Decrease capacity by one ,call event.decrease_capacity()
        if self.capacity > 0:
            self.capacity -= 1
            self.save()
        else:
            raise ValueError("No available spots left for this event.")
from django.utils import timezone
from django.db import models
from django.core.validators import MaxValueValidator
from accounts.models import HostProfile
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

# Create your models here.
class Event(models.Model):
    #host = models.ForeignKey('accounts.HostProfile', on_delete=models.CASCADE, related_name='hosted_events') #will be used in source in the host serializer
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField(validators=[MaxValueValidator(50)])
    created_date = models.DateTimeField(auto_now_add=True)
    # One-to-many relationship with HostProfile
    host = models.ForeignKey(HostProfile, on_delete=models.CASCADE, related_name='events_hosted')
    # Many-to-many relationship with CustomUser
    attendees = models.ManyToManyField(User, related_name='events_attending')

    def __str__(self):
        return f"{self.title} hosted by {self.host.user.username} from {self.host.organization}"
    

    def save(self, *args, **kwargs):
        # Ensure the event is not scheduled in the past
        if self.date_time < timezone.now():
            raise ValidationError("Event cannot be scheduled in the past.")
        super(Event, self).save(*args, **kwargs)

    def decrease_capacity(self):
        # Decrease capacity by one ,call event.decrease_capacity()
        if self.capacity > 0:
            self.capacity -= 1
            self.save()
        else:
            raise ValidationError("No available spots left for this event.")
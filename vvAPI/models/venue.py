from django.db import models
from django.contrib.auth.models import User #pylint:disable=imported-auth-user
from vvAPI.models.event import Event



class Venue(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    state = models.ForeignKey('State', on_delete=models.CASCADE)

    @property
    def venue_events(self):
        event = Event.objects.filter(venue=self)
        return event

    def __str__(self):
        return self.name
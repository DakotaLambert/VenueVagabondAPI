from django.db import models
# from vvAPI.models.venue import Venue
from vvAPI.models.event_image import EventImage


class Event(models.Model):
    name = models.CharField(max_length=500)
    event_type = models.ForeignKey('EventType', null=True, on_delete=models.SET_NULL)
    venue = models.ForeignKey('Venue', on_delete=models.CASCADE)
    date_of_event = models.DateField()

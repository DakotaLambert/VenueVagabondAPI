from django.db import models
from vvAPI.models.venue import Venue

class State(models.Model):
    """[summary]

    Args:
        models ([type]): [description]
    """
    name = models.CharField(max_length=60)
    abbreviation = models.CharField(max_length=10)

    @property
    def state_venues(self):
        venue = Venue.objects.filter(state=self)
        return venue
    

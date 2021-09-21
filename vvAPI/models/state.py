from django.db import models
from vvAPI.models.venue import Venue

class State(models.Model):
    """[summary]

    Args:
        models ([type]): [description]
    """
    name = models.CharField(max_length=60)
    abbreviation = models.CharField(max_length=10)

    def get_state_venues(self, user):
        venues = Venue.objects.filter(state=self, user=user)
        return venues

    @property
    def state_venues(self):
        return self.__state_venues
    @state_venues.setter
    def state_venues(self, value):
        self.__state_venues = value
from django.db import models
from django.db.models.deletion import DO_NOTHING


class Venue(models.Model):

    name = models.CharField(max_length=200)
    state = models.ForeignKey('State', on_delete=DO_NOTHING)

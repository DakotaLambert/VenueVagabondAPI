from django.db import models
from django.contrib.auth.models import User #pylint:disable=imported-auth-user


class Venue(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    state = models.ForeignKey('State', on_delete=models.CASCADE)

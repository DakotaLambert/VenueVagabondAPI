from django.db import models
from django.contrib.auth.models import User #pylint:disable=imported-auth-user


class EventType(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
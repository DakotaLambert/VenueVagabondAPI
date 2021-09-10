from django.db import models
from django.contrib.auth.models import User #pylint:disable=imported-auth-user


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    image_path = models.ImageField(upload_to="image", height_field=None, width_field=None, max_length=None, null=True)
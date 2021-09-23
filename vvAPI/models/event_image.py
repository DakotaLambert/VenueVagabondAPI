from django.db import models


class EventImage(models.Model):
    user = models.ForeignKey('VVUser', on_delete=models.DO_NOTHING)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image", height_field=None, width_field=None, max_length=None, null=True)


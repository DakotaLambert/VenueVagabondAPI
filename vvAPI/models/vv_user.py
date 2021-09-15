from django.db import models
from django.contrib.auth.models import User #pylint:disable=imported-auth-user

class VVUser(models.Model):
    """[summary]

    Args:
        models ([type]): [description]
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.ForeignKey('State', on_delete=models.DO_NOTHING)
    image_url = models.ImageField(upload_to="image", height_field=None, width_field=None, max_length=None, null=True)

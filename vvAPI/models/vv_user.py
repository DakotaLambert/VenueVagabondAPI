from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.contrib.auth.models import User #pylint:disable=imported-auth-user

class VVUser(models.Model):
    """[summary]

    Args:
        models ([type]): [description]
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.ForeignKey('State', on_delete=DO_NOTHING)

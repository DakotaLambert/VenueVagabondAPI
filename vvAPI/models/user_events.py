from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.contrib.auth.models import User #pylint:disable=imported-auth-user

#? Which way does CASCADE work

class UserEvent(models.Model):
    """[summary]

    Args:
        models ([type]): [description]
    """
    user = models.ForeignKey(User, on_delete=DO_NOTHING)
    event = models.ForeignKey('Event', on_delete=DO_NOTHING)

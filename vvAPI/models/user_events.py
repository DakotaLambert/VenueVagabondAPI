from django.db import models

#? Which way does CASCADE work

class UserEvent(models.Model):
    """[summary]

    Args:
        models ([type]): [description]
    """
    user = models.ForeignKey('VVUser', on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)

from django.db import models

class State(models.Model):
    """[summary]

    Args:
        models ([type]): [description]
    """
    name = models.CharField(max_length=60)
    abbreviation = models.CharField(max_length=10)
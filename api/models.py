"""
Model which contains all of the models used by our application
"""

from django.db import models


class Call(models.Model):
    """
    Database model for the telephone calls.

    Attributes:
        source (models.CharField): telephone number of the source
        destination (models.CharField): telephone number of the destination

    """
    source = models.CharField(max_length=11, required=True)
    destination = models.CharField(max_length=11, required=True)

    def __str__(self):
        return str(self.id)

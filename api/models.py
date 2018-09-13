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
    source = models.CharField(max_length=11)
    destination = models.CharField(max_length=11)

    def __str__(self):
        return str(self.id)


class CallDetail(models.Model):
    """
    Database model for the details of a telephone call.telephone

    Attributes:
        call_id (Call.id): the foreign key from Call
        start (models.BooleanField): start (True) or end (False) of a call
        timestamp (models.DateTimeField): when the call was started or finished

    """
    call_id = models.ForeignKey('Call', on_delete=models.CASCADE)
    start = models.BooleanField(default=True)
    timestamp = models.DateTimeField()

    def __str__(self):
        return str(self.id)

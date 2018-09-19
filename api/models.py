"""
Model which contains the models used by our application
"""

from django.db import models
from datetime import datetime


class Call(models.Model):
    """
    Telephone calls.

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
    Details of a telephone call.

    Attributes:
        call_id (Call.id): the foreign key from Call
        start (models.BooleanField): start (True) or end (False) of a call
        timestamp (models.DateTimeField): when the call was started or finished

    """
    call_id = models.ForeignKey('Call', on_delete=models.CASCADE)
    start = models.BooleanField(default=True, blank=False)
    timestamp = models.DateTimeField()

    def __str__(self):
        return str(self.id)


class PriceRule(models.Model):
    """
    Rules to calculate a price

    Attributes:
        created_date (models.DateTimeField): Date time of the rule creation
    """
    created_date = models.DateTimeField(default=datetime.now, blank=False)

    def __str__(self):
        return str(self.id)


class PriceRuleDetail(models.Model):
    """
    Details of a rule to calculate a price

    Attributes:
        price_id (models.ForeignKey): price rule id
        standing_charge (models.FloatField): fixed charge value
        call_charge (models.FloatField): value charged by minute
        start (models.TimeField): start time of the price rule period
        end (models.TimeField): end time of the price rule period
    """
    price_id = models.ForeignKey('PriceRule', on_delete=models.CASCADE)
    standing_charge = models.FloatField(default=0.0, blank=False)
    call_charge = models.FloatField(default=0.0, blank=False)
    start = models.TimeField(blank=False)
    end = models.TimeField(blank=False)

    def __str__(self):
        return str(self.id)

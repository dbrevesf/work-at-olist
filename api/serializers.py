"""
Serializers module.
"""
from .models import Call
from rest_framework import serializers


class CallSerializer(serializers.ModelSerializer):
    """
    Serializer for the model Call.
    """
    class Meta:
        model = Call
        fields = ('id', 'source', 'destination')

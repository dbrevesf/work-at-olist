"""
Serializers module.
"""
from .models import Call
from .models import CallDetail
from .models import PriceRule
from rest_framework import serializers


class CallSerializer(serializers.ModelSerializer):
    """
    Serializer for the model Call.
    """
    class Meta:
        model = Call
        fields = ('id', 'source', 'destination')


class CallDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the model CallDetail.
    """
    class Meta:
        model = CallDetail
        fields = ('id', 'call_id', 'start', 'timestamp')


class PriceRuleSerializer(serializers.ModelSerializer):
    """
    Serializer for the model PriceRule
    """
    class Meta:
        model = PriceRule
        fields = ('id', 'created_date')

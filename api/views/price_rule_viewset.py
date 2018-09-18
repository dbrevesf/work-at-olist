from api.models import PriceRule
from api.serializers import PriceRuleSerializer
from rest_framework import viewsets


class PriceRuleViewSet(viewsets.ModelViewSet):
    """
    API endpoint to PriceRule
    """
    queryset = PriceRule.objects.all()
    serializer_class = PriceRuleSerializer

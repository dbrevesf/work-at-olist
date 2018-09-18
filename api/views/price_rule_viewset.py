from api.models import PriceRule
from api.serializers import PriceRuleSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response


class PriceRuleViewSet(viewsets.ModelViewSet):
    """
    API endpoint to PriceRule
    """
    queryset = PriceRule.objects.all()
    serializer_class = PriceRuleSerializer

    def __validate_input(self, request_data):
        """
        Method to validate the inputs for the API endpoint PriceRule.

        Parameters:

            request_data (Dictonary): Request data sent by the HTTP request

        Return:

            validation (Dictionary): Dictionary with error/success message.
        """
        created_date = request_data.get('created_date')
        price_rules = PriceRule.objects
        validation = None
        if created_date:
            stored_price_rule = price_rules.filter(created_date=created_date)
            if stored_price_rule:
                validation = {'input_error':
                              'two price rules with the same time date'}

        return validation

    def create(self, request):

        validation = self.__validate_input(request.data)
        response = None
        if validation:
            response = Response(validation, status.HTTP_400_BAD_REQUEST)
        else:
            response = super(PriceRuleViewSet, self).create(request)
        return response

    def update(self, request, pk=None):

        validation = self.__validate_input(request.data)
        response = None
        if validation:
            response = Response(validation, status.HTTP_400_BAD_REQUEST)
        else:
            response = super(PriceRuleViewSet, self).update(request, pk)
        return response

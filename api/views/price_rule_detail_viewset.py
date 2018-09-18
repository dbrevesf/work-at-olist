from api.models import PriceRuleDetail
from api.serializers import PriceRuleDetailSerializer
from api.utils import standardize_date
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime

TIME_PATTERN = '%H:%M'


class PriceRuleDetailViewSet(viewsets.ModelViewSet):
    """
    API endpoint to PriceRule
    """
    queryset = PriceRuleDetail.objects.all()
    serializer_class = PriceRuleDetailSerializer

    def validate_input(self, request_data):
        """
        Method to validate the inputs for the API endpoint PriceRuleDetail.

        Parameters:

            request_data (Dictonary): Request data sent by the HTTP request

        Return:

            validation (Dictionary): Dictionary with error/success message.
        """
        validation = None
        start = request_data.get('start')
        end = request_data.get('end')
        standing_charge = request_data.get('standing_charge')
        call_charge = request_data.get('call_charge')
        price_id = request_data.get('price_id')
        if start and end and standing_charge and call_charge:
            start = standardize_date(start, TIME_PATTERN)
            end = standardize_date(end, TIME_PATTERN)
            if isinstance(start, datetime) and isinstance(end, datetime):
                if start >= end:
                    validation = {'input_error':
                                  'end must be later than start'}
                else:
                    check = self.check_time_conflicts(price_id, start, end)
                    if not check:
                        error_message = 'time conflict between the rules'
                        validation = {'input_error': error_message}
            else:
                validation = {'input_error': 'wrong time format'}
            if float(standing_charge) < 0.0 or float(call_charge) < 0.0:
                validation = {'input_error': 'charges must be positive'}

        return validation

    def check_time_conflicts(self, price_id, start, end):

        response = True
        if price_id:
            price_rules = PriceRuleDetail.objects.filter(price_id=price_id)
            if len(price_rules) > 0:
                time_interval = []
                response = False
                for rule in price_rules:
                    time_interval.append(rule.start)
                    time_interval.append(rule.end)
                if start.time() > max(time_interval):
                    response = True
        return response

    def create(self, request):

        response = None
        validation = self.validate_input(request.data)
        if validation:
            response = Response(validation, status.HTTP_400_BAD_REQUEST)
        else:
            response = super(PriceRuleDetailViewSet, self).create(request)

        return response

    def update(self, request, pk=None):

        response = None
        validation = self.validate_input(request.data)
        if validation:
            response = Response(validation, status.HTTP_400_BAD_REQUEST)
        else:
            response = super(PriceRuleDetailViewSet, self).update(request, pk)
        return response

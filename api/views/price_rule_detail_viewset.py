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

    def __validate_input(self, request_data):
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
                if start == end:
                    validation = {'input_error':
                                  'end must be different than start'}
                else:
                    time_conflicts = self.__check_time_conflicts(price_id,
                                                                 start.time(),
                                                                 end.time())
                    if time_conflicts:
                        error_message = 'time conflict between the rules'
                        validation = {'input_error': error_message}
            else:
                validation = {'input_error': 'wrong time format'}
            if float(standing_charge) < 0.0 or float(call_charge) < 0.0:
                validation = {'input_error': 'charges must be positive'}

        return validation

    def __check_time_conflicts(self, price_id, start, end):

        conflict = False
        if price_id:
            price_rules = PriceRuleDetail.objects.filter(price_id=price_id)
            if len(price_rules) > 0:
                for rule in price_rules:
                    if rule.start > rule.end:
                        if start > end:
                            conflict = True
                            break
                        else:
                            if rule.start <= start or start <= rule.end:
                                conflict = True
                                break
                            elif rule.start <= end or end <= rule.end:
                                conflict = True
                                break
                            else:
                                conflict = False
                    else:
                        if rule.start <= start <= rule.end:
                            conflict = True
                            break
                        elif rule.start <= end <= rule.end:
                            conflict = True
                            break
                        else:
                            conflict = False
        return conflict

    def create(self, request):

        response = None
        validation = self.__validate_input(request.data)
        if validation:
            response = Response(validation, status.HTTP_400_BAD_REQUEST)
        else:
            response = super(PriceRuleDetailViewSet, self).create(request)

        return response

    def update(self, request, pk=None):

        response = None
        validation = self.__validate_input(request.data)
        if validation:
            response = Response(validation, status.HTTP_400_BAD_REQUEST)
        else:
            response = super(PriceRuleDetailViewSet, self).update(request, pk)
        return response

from api import strings
from api import utils
from api.models import PriceRuleDetail
from api.serializers import PriceRuleDetailSerializer
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime


class PriceRuleDetailViewSet(viewsets.ModelViewSet):
    """
    API endpoint to PriceRule
    """
    queryset = PriceRuleDetail.objects.all()
    serializer_class = PriceRuleDetailSerializer

    def __validate_input(self, request_data):
        """
        Validate the inputs for the API endpoint PriceRuleDetail.

        Parameters:

            request_data (Dictonary): Request data sent by the HTTP request

        Return:

            validation (Dictionary): Dictionary with error/success message.
        """
        validation = None
        start = request_data.get(strings.START_KEY)
        end = request_data.get(strings.END_KEY)
        standing_charge = request_data.get(strings.STANDING_CHARGE_KEY)
        call_charge = request_data.get(strings.CALL_CHARGE_KEY)
        price_id = request_data.get(strings.PRICE_ID_KEY)
        if start and end and standing_charge and call_charge:
            start = utils.standardize_date(start, strings.TIME_PATTERN)
            end = utils.standardize_date(end, strings.TIME_PATTERN)
            if isinstance(start, datetime) and isinstance(end, datetime):
                if start == end:
                    validation = {strings.INPUT_ERROR_KEY:
                                  strings.END_EQUAL_START_ERROR}
                else:
                    time_conflicts = self.__check_time_conflicts(price_id,
                                                                 start.time(),
                                                                 end.time())
                    if time_conflicts:
                        validation = {strings.INPUT_ERROR_KEY:
                                      strings.RULES_TIME_CONFLICT_ERROR}
            else:
                validation = {strings.INPUT_ERROR_KEY:
                              strings.TIME_FORMAT_ERROR}
            if float(standing_charge) < 0.0 or float(call_charge) < 0.0:
                validation = {strings.INPUT_ERROR_KEY:
                              strings.NEGATIVE_CHARGES_ERROR}
        return validation

    def __check_time_conflicts(self, price_id, start, end):
        """
        Verify if a rule will not conflict with another due to the time period.

        Parameters:
            price_id (int): PriceRuleDetail identification
            start (datetime.datetime): start period of the rule detail
            end (datetime.datetime): end period of the rule detail

        Return:
            conflict (boolean): True if there's a conflict or False.

        """
        conflict = False
        if price_id:
            price_rules = PriceRuleDetail.objects.filter(price_id=price_id)
            if len(price_rules):
                for rule in price_rules:
                    if rule.start > rule.end:
                        if start > end:
                            conflict = True
                            break
                        else:
                            if rule.start <= start or start < rule.end:
                                conflict = True
                                break
                            elif rule.start < end or end <= rule.end:
                                conflict = True
                                break
                            else:
                                conflict = False
                    else:
                        if rule.start <= start < rule.end:
                            conflict = True
                            break
                        elif rule.start < end <= rule.end:
                            conflict = True
                            break
                        else:
                            conflict = False
        return conflict

    def create(self, request):
        """
        POST /api/priceruledetail/
        """
        response = None
        validation = self.__validate_input(request.data)
        if validation:
            response = Response(validation, status.HTTP_400_BAD_REQUEST)
        else:
            response = super(PriceRuleDetailViewSet, self).create(request)

        return response

    def update(self, request, pk=None):
        """
        PUT /api/priceruledetail/<pk>/
        """
        response = None
        validation = self.__validate_input(request.data)
        if validation:
            response = Response(validation, status.HTTP_400_BAD_REQUEST)
        else:
            response = super(PriceRuleDetailViewSet, self).update(request, pk)
        return response

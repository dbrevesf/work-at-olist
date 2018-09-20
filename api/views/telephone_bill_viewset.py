from api import utils
from api import strings
from api.models import CallDetail
from api.models import PriceRule
from api.models import PriceRuleDetail
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
import datetime


class TelephoneBillViewSet(viewsets.ViewSet):
    """
    API endpoint to TelephoneBill
    """

    def __get_call_bill(self, call):
        """
        Method to get the bill for a call.

        Parameters:
            call (dictionary): dictionary containing the call informations
            used to calculate the bill.

        return:
            response (dictionary): if the bill was correctly calculated, this
            method will return the bill inside a dictionary with a success
            message. Otherwise, a error message informing the error cause will
            be sent.
        """
        response = None
        call_id = list(call.keys())[0]
        call = call.get(call_id)
        start = utils.standardize_date(call.get(strings.START_KEY),
                                       strings.COMPLETE_DATE_PATTERN)
        end = utils.standardize_date(call.get(strings.END_KEY),
                                     strings.COMPLETE_DATE_PATTERN)
        destination = call.get(strings.DESTINATION_KEY)
        total = end - start
        total_minutes = ((total.days * 24 * 60) + (total.seconds // 60))
        hours = (total.days * 24) + (total.seconds / (60 * 60))
        minutes = (total.seconds % (60 * 60)) / 60
        seconds = total.seconds % 60
        duration = (strings.HOUR_MINUTE_SECOND_PATTERN %
                    (hours, minutes, seconds))
        call_bill = {strings.DESTINATION_KEY: destination,
                     strings.START_DATE_KEY: start.date(),
                     strings.START_TIME_KEY: start.time(),
                     strings.DURATION_KEY: duration}
        price_rules = PriceRule.objects.filter(
            created_date__lt=end).order_by('-id')
        price_rule = None
        if price_rules:
            price_rule = price_rules[0]
            price_rule_details = PriceRuleDetail.objects.filter(
                price_id=price_rule.id)
            final_price = 0
            left_time = total_minutes
            while left_time > 0:
                selected_rule = self.__select_price_rule(start,
                                                         price_rule_details)
                if selected_rule:
                    rule_period = utils.get_period_between_time(
                        selected_rule.start,
                        selected_rule.end)
                    left_time = total_minutes - rule_period
                    if left_time >= 0:
                        start += datetime.timedelta(seconds=rule_period * 60)
                        total_minutes -= rule_period
                        final_price += (selected_rule.standing_charge +
                                        rule_period *
                                        selected_rule.call_charge)
                    else:
                        final_price += (selected_rule.standing_charge +
                                        total_minutes *
                                        selected_rule.call_charge)
                    call_bill[strings.PRICE_KEY] = round(final_price, 2)
                    response = {strings.SUCCESS_KEY: call_bill}
                else:
                    left_time = 0
                    response = {strings.ERROR_KEY: strings.NO_PRICE_RULE_ERROR}
        else:
            response = {strings.ERROR_KEY: strings.NO_PRICE_RULE_ERROR}
        return response

    def __get_period_calls(self, source, period):
        """
        Method to get all the calls of the same source for a given period.

        Parameters:
            source (string): the source number of the calls
            period (string): the period in the YYYY-MM format informing the
            month and the year that we want to get the calls.

        Return
            period_calls (list): a list of calls if it exists, or an empty
            list.
        """
        call_details = CallDetail.objects.filter(call_id__source=source)
        period_calls = []
        if call_details:
            call_data = {}
            for call_detail in call_details:
                check_same_year = call_detail.timestamp.year == period.year
                check_same_month = call_detail.timestamp.month == period.month
                if check_same_month and check_same_year:
                    call_id = call_detail.call_id.id
                    destination = call_detail.call_id.destination
                    if call_id not in call_data.keys():
                        call_data[call_id] = {}
                    if call_detail.start:
                        call_data[call_id][strings.START_KEY] =\
                            call_detail.timestamp
                    else:
                        call_data[call_id][strings.END_KEY] =\
                            call_detail.timestamp
                    call_data[call_id][strings.DESTINATION_KEY] = destination
                    check_start = call_data[call_id].get(strings.START_KEY)
                    check_end = call_data[call_id].get(strings.END_KEY)
                    if check_start and check_end:
                        period_calls.append(call_data)
                        call_data = {}
        return period_calls

    def __select_price_rule(self, start, price_rule_details):
        """
        Method to select a price rule from a list of price rules, according to
        the call start.

        Parameters:
            start (datetime.time) - when the call started
            price_rule_details - list of price rules

        Return:
            selected_rule (PriceRuleDetail) - the selected rule or None.
        """
        selected_rule = None
        for rule_detail in price_rule_details:
            if rule_detail.start > rule_detail.end:
                if not (rule_detail.end < start.time() <
                        rule_detail.start):
                    selected_rule = rule_detail
                    break
            else:
                if rule_detail.start <= start.time() < rule_detail.end:
                    selected_rule = rule_detail
                    break
        return selected_rule

    def list(self, request):
        """
        GET /api/telephonebill?source=<source>&period=<period-optional>
        """
        response = None
        source = request.query_params.get(strings.SOURCE_KEY)
        if source:
            period = request.query_params.get(strings.PERIOD_KEY)
            if not period:
                period = utils.get_last_month_period()
            period = utils.standardize_date(period, strings.YEAR_MONTH_PATTERN)
            period_calls = self.__get_period_calls(source, period)
            bill_list = []
            for call in period_calls:
                bill = self.__get_call_bill(call)
                if bill:
                    bill_list.append(bill)
            if bill_list:
                response = Response(bill_list, status.HTTP_200_OK)
            else:
                content = {strings.ERROR_KEY: strings.BILLS_NOT_FOUND_ERROR}
                response = Response(content, status.HTTP_404_NOT_FOUND)
        else:
            content = {strings.INPUT_ERROR_KEY: strings.SOURCE_MISSED_ERROR}
            response = Response(content, status.HTTP_400_BAD_REQUEST)
        return response

"""
Module containing the unit tests of the API endpoint TelephoneBill
"""
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status


class TelephoneBillTest(APITestCase):
    """
    Class which contains the unit tests for the API endpoint: TelephoneBill
    """
    url = '/api/telephonebill/'
    client = APIClient()

    def test_get_telephone_bill(self):
        pass

    def test_get_telephone_bill_without_period(self):
        pass

    def test_get_telephone_bill_without_source(self):
        pass

    def test_get_telephone_bill_with_small_price_rule(self):
        pass

    def test_get_telephone_bill_with_large_price_rule(self):
        pass

    def test_get_telephone_bill_with_long_calls(self):
        pass

    def test_get_telephone_bill_with_short_calls(self):
        pass

    def test_get_telephone_bill_with_extra_long_calls(self):
        pass

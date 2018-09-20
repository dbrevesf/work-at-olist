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
    price_rule_url = '/api/pricerule/'
    price_rule_detail_url = '/api/priceruledetail/'
    call_url = '/api/call/'
    call_detail_url = '/api/calldetail/'
    client = APIClient()
    source = '19988271648'

    def create_regular_call(self):

        call_data = {'source': self.source, 'destination': '1982312312'}
        call = self.client.post(self.call_url, call_data, format='json')
        call_details_data = {'call_id': call.data['id'],
                             'start': True,
                             'timestamp': '2018-08-14T01:16:54Z'}
        self.client.post(self.call_detail_url,
                         call_details_data,
                         format='json')
        call_details_data = {'call_id': call.data['id'],
                             'start': False,
                             'timestamp': '2018-08-14T01:26:54Z'}
        self.client.post(self.call_detail_url,
                         call_details_data,
                         format='json')

    def create_long_call(self):

        call_data = {'source': self.source, 'destination': '1982312312'}
        call = self.client.post(self.call_url, call_data, format='json')
        call_details_data = {'call_id': call.data['id'],
                             'start': True,
                             'timestamp': '2017-08-14T00:00:00Z'}
        self.client.post(self.call_detail_url,
                         call_details_data,
                         format='json')
        call_details_data = {'call_id': call.data['id'],
                             'start': False,
                             'timestamp': '2017-08-15T8:00:00Z'}
        self.client.post(self.call_detail_url,
                         call_details_data,
                         format='json')

    def create_short_call(self):

        call_data = {'source': self.source, 'destination': '1982312312'}
        call = self.client.post(self.call_url, call_data, format='json')
        call_details_data = {'call_id': call.data['id'],
                             'start': True,
                             'timestamp': '2018-08-14T01:16:54Z'}
        self.client.post(self.call_detail_url,
                         call_details_data,
                         format='json')
        call_details_data = {'call_id': call.data['id'],
                             'start': False,
                             'timestamp': '2018-08-14T01:17:54Z'}
        self.client.post(self.call_detail_url,
                         call_details_data,
                         format='json')

    def create_regular_price_rule(self):

        data = {'created_date': '2000-09-13T19:18:43Z'}
        response = self.client.post(self.price_rule_url, data, format='json')
        price_rule_id = response.data.get('id')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.50,
                'call_charge': 0.40,
                'start': '00:00',
                'end': '23:59'}
        self.client.post(self.price_rule_detail_url, data, format='json')

    def create_long_price_rule(self):

        data = {'created_date': '2000-09-13T19:18:43Z'}
        response = self.client.post(self.price_rule_url, data, format='json')
        price_rule_id = response.data.get('id')
        data = {'price_id': price_rule_id,
                'standing_charge': 1,
                'call_charge': 1,
                'start': '00:00',
                'end': '08:00'}
        self.client.post(self.price_rule_detail_url, data, format='json')
        data = {'price_id': price_rule_id,
                'standing_charge': 2,
                'call_charge': 2,
                'start': '08:00',
                'end': '16:00'}
        self.client.post(self.price_rule_detail_url, data, format='json')
        data = {'price_id': price_rule_id,
                'standing_charge': 3,
                'call_charge': 3,
                'start': '16:00',
                'end': '00:00'}
        self.client.post(self.price_rule_detail_url, data, format='json')

    def test_get_telephone_bill(self):

        self.create_regular_call()
        self.create_regular_price_rule()
        period = '2018-08'
        parameter_url = '%s?source=%s&period=%s' % (self.url,
                                                    self.source,
                                                    period)
        response = self.client.get(parameter_url, format='json')

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['price'], 4.5)

    def test_get_telephone_bill_without_period(self):

        self.create_regular_call()
        self.create_regular_price_rule()
        parameter_url = '%s?source=%s&period=%s' % (self.url,
                                                    self.source,
                                                    '')
        response = self.client.get(parameter_url, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['price'], 4.5)

    def test_get_telephone_bill_without_source(self):

        self.create_regular_call()
        self.create_regular_price_rule()
        period = '2018-08'
        parameter_url = '%s?source=%s&period=%s' % (self.url,
                                                    '',
                                                    period)
        response = self.client.get(parameter_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_telephone_bill_with_long_calls(self):

        self.create_long_call()
        self.create_long_price_rule()
        period = '2017-08'
        parameter_url = '%s?source=%s&period=%s' % (self.url,
                                                    self.source,
                                                    period)
        response = self.client.get(parameter_url, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['price'], 3367.0)

    def test_get_telephone_bill_with_short_calls(self):

        self.create_short_call()
        self.create_regular_price_rule()
        period = '2018-08'
        parameter_url = '%s?source=%s&period=%s' % (self.url,
                                                    self.source,
                                                    period)
        response = self.client.get(parameter_url, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['price'], 0.90)


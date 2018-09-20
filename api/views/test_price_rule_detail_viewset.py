"""
Module containing the unit tests of the API endpoint PriceRule
"""
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status


class PriceRuleDetailTest(APITestCase):
    """
    Class which contains the unit tests for the API endpoint: PriceRule
    """
    price_rule_url = '/api/pricerule/'
    url = '/api/priceruledetail/'
    client = APIClient()

    def test_create_price_rule_detail(self):

        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.price_rule_url, data, format='json')
        price_rule_id = response.data.get('id')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.39,
                'call_charge': 0.40,
                'start': '00:00',
                'end': '08:00'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_empty_price_rule_detail(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_price_rule_detail_without_price_id(self):

        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.price_rule_url, data, format='json')
        data = {'price_id': '',
                'standing_charge': 0.39,
                'call_charge': 0.40,
                'start': '00:00',
                'end': '08:00'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_price_rule_detail_without_standing_charge(self):

        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.price_rule_url, data, format='json')
        price_rule_id = response.data.get('id')
        data = {'price_id': price_rule_id,
                'standing_charge': '',
                'call_charge': 0.40,
                'start': '00:00',
                'end': '08:00'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_price_rule_detail_without_call_charge(self):

        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.price_rule_url, data, format='json')
        price_rule_id = response.data.get('id')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.30,
                'call_charge': '',
                'start': '00:00',
                'end': '08:00'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_price_rule_detail_without_start(self):

        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.price_rule_url, data, format='json')
        price_rule_id = response.data.get('id')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.30,
                'call_charge': 0.40,
                'start': '',
                'end': '08:00'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_price_rule_detail_without_end(self):

        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.price_rule_url, data, format='json')
        price_rule_id = response.data.get('id')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.30,
                'call_charge': 0.40,
                'start': '00:00',
                'end': ''}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_price_rule_detail_with_start_equal_end(self):

        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.price_rule_url, data, format='json')
        price_rule_id = response.data.get('id')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.30,
                'call_charge': 0.40,
                'start': '08:00',
                'end': '08:00'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_two_price_rule_details(self):

        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.price_rule_url, data, format='json')
        price_rule_id = response.data.get('id')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.30,
                'call_charge': 0.40,
                'start': '22:00',
                'end': '06:00'}
        response = self.client.post(self.url, data, format='json')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.30,
                'call_charge': 0.40,
                'start': '06:01',
                'end': '21:59'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_two_price_rule_details_with_conflict(self):

        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.price_rule_url, data, format='json')
        price_rule_id = response.data.get('id')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.30,
                'call_charge': 0.40,
                'start': '22:00',
                'end': '06:00'}
        response = self.client.post(self.url, data, format='json')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.30,
                'call_charge': 0.40,
                'start': '05:00',
                'end': '21:59'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_three_price_rule_details_with_conflict(self):

        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.price_rule_url, data, format='json')
        price_rule_id = response.data.get('id')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.30,
                'call_charge': 0.40,
                'start': '22:00',
                'end': '06:00'}
        response = self.client.post(self.url, data, format='json')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.30,
                'call_charge': 0.40,
                'start': '07:00',
                'end': '10:00'}
        response = self.client.post(self.url, data, format='json')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.30,
                'call_charge': 0.40,
                'start': '20:00',
                'end': '3:00'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_three_price_rule_details(self):

        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.price_rule_url, data, format='json')
        price_rule_id = response.data.get('id')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.30,
                'call_charge': 0.40,
                'start': '22:00',
                'end': '06:00'}
        response = self.client.post(self.url, data, format='json')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.30,
                'call_charge': 0.40,
                'start': '07:00',
                'end': '10:00'}
        response = self.client.post(self.url, data, format='json')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.30,
                'call_charge': 0.40,
                'start': '11:00',
                'end': '20:00'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_price_rule_detail_with_negative_standing_charge(self):

        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.price_rule_url, data, format='json')
        price_rule_id = response.data.get('id')
        data = {'price_id': price_rule_id,
                'standing_charge': -0.30,
                'call_charge': 0.40,
                'start': '00:00',
                'end': '08:00'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_price_rule_detail_with_negative_call_charge(self):
        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.price_rule_url, data, format='json')
        price_rule_id = response.data.get('id')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.30,
                'call_charge': -0.40,
                'start': '00:00',
                'end': '08:00'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_price_rule_detail_without_price_id(self):

        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.price_rule_url, data, format='json')
        price_rule_id = response.data.get('id')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.39,
                'call_charge': 0.40,
                'start': '00:00',
                'end': '08:00'}
        response = self.client.post(self.url, data, format='json')
        price_rule_detail_id = response.data.get('id')
        price_rule_detail_url = self.url + str(price_rule_detail_id) + '/'
        data['price_id'] = ''
        response = self.client.put(price_rule_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_price_rule_detail_without_standing_charge(self):

        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.price_rule_url, data, format='json')
        price_rule_id = response.data.get('id')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.39,
                'call_charge': 0.40,
                'start': '00:00',
                'end': '08:00'}
        response = self.client.post(self.url, data, format='json')
        price_rule_detail_id = response.data.get('id')
        price_rule_detail_url = self.url + str(price_rule_detail_id) + '/'
        data['standing_charge'] = ''
        response = self.client.put(price_rule_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_price_rule_detail_without_call_charge(self):

        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.price_rule_url, data, format='json')
        price_rule_id = response.data.get('id')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.39,
                'call_charge': 0.40,
                'start': '00:00',
                'end': '08:00'}
        response = self.client.post(self.url, data, format='json')
        price_rule_detail_id = response.data.get('id')
        price_rule_detail_url = self.url + str(price_rule_detail_id) + '/'
        data['call_charge'] = ''
        response = self.client.put(price_rule_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_price_rule_detail_without_start(self):

        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.price_rule_url, data, format='json')
        price_rule_id = response.data.get('id')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.39,
                'call_charge': 0.40,
                'start': '00:00',
                'end': '08:00'}
        response = self.client.post(self.url, data, format='json')
        price_rule_detail_id = response.data.get('id')
        price_rule_detail_url = self.url + str(price_rule_detail_id) + '/'
        data['start'] = ''
        response = self.client.put(price_rule_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_price_rule_detail_without_end(self):

        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.price_rule_url, data, format='json')
        price_rule_id = response.data.get('id')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.39,
                'call_charge': 0.40,
                'start': '00:00',
                'end': '08:00'}
        response = self.client.post(self.url, data, format='json')
        price_rule_detail_id = response.data.get('id')
        price_rule_detail_url = self.url + str(price_rule_detail_id) + '/'
        data['end'] = ''
        response = self.client.put(price_rule_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_price_rule_detail_with_start_equal_end(self):

        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.price_rule_url, data, format='json')
        price_rule_id = response.data.get('id')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.39,
                'call_charge': 0.40,
                'start': '00:00',
                'end': '08:00'}
        response = self.client.post(self.url, data, format='json')
        price_rule_detail_id = response.data.get('id')
        price_rule_detail_url = self.url + str(price_rule_detail_id) + '/'
        data['start'] = data['end']
        response = self.client.put(price_rule_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_price_rule_detail_with_conflict_with_another_rule(self):

        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.price_rule_url, data, format='json')
        price_rule_id = response.data.get('id')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.30,
                'call_charge': 0.40,
                'start': '00:00',
                'end': '08:00'}
        response = self.client.post(self.url, data, format='json')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.30,
                'call_charge': 0.40,
                'start': '08:01',
                'end': '11:00'}
        response = self.client.post(self.url, data, format='json')
        price_rule_detail_id = response.data.get('id')
        price_rule_detail_url = self.url + str(price_rule_detail_id) + '/'
        data['start'] = '08:00'
        response = self.client.put(price_rule_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_price_rule_detail_with_negative_standing_charge(self):

        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.price_rule_url, data, format='json')
        price_rule_id = response.data.get('id')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.39,
                'call_charge': 0.40,
                'start': '00:00',
                'end': '08:00'}
        response = self.client.post(self.url, data, format='json')
        price_rule_detail_id = response.data.get('id')
        price_rule_detail_url = self.url + str(price_rule_detail_id) + '/'
        data['standing_charge'] = -0.40
        response = self.client.put(price_rule_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_price_rule_detail_with_negative_call_charge(self):

        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.price_rule_url, data, format='json')
        price_rule_id = response.data.get('id')
        data = {'price_id': price_rule_id,
                'standing_charge': 0.39,
                'call_charge': 0.40,
                'start': '00:00',
                'end': '08:00'}
        response = self.client.post(self.url, data, format='json')
        price_rule_detail_id = response.data.get('id')
        price_rule_detail_url = self.url + str(price_rule_detail_id) + '/'
        data['call_charge'] = -0.23
        response = self.client.put(price_rule_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

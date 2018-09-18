"""
Module containing the unit tests of the API endpoint PriceRule
"""
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status


class PriceRuleTest(APITestCase):
    """
    Class which contains the unit tests for the API endpoint: PriceRule
    """
    url = '/api/pricerule/'
    client = APIClient()

    def test_create_price_rule(self):
        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_empty_price_rules(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_price_rule_without_date(self):
        data = {'created_date': ''}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_price_rule_with_wrong_format_date(self):
        data = {'created_date': '2018-09-12'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_price_rules_with_same_date(self):
        data = {'created_date': '2018-09-13T19:18:43Z'}
        self.client.post(self.url, data, format='json')
        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_price_rules_with_same_date(self):
        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.url, data, format='json')
        price_rule_id = response.data.get('id')
        price_rule_url = self.url + str(price_rule_id) + '/'
        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.put(price_rule_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_a_single_price_rule(self):
        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.url, data, format='json')
        price_rule_id = response.data.get('id')
        price_rule_url = self.url + str(price_rule_id) + '/'
        response = self.client.get(price_rule_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), price_rule_id)

    def delete_a_single_price_rule(self):
        data = {'created_date': '2018-09-13T19:18:43Z'}
        response = self.client.post(self.url, data, format='json')
        price_rule_id = response.data.get('id')
        price_rule_url = self.url + str(price_rule_id) + '/'
        response = self.client.delete(price_rule_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

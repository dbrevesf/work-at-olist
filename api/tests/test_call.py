"""
Module containing the unit tests of the API endpoints
"""
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status


class CallTest(APITestCase):
    """
    Class which contains the unit tests for the API endpoint: Call
    """

    url = '/api/call/'
    client = APIClient()

    def test_list_calls(self):

        data = {'source': '19988271648', 'destination': '1988271616'}
        self.client.post(self.url, data, format='json')
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_empty_calls(self):

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_existent_unique_call(self):

        data = {'source': '19988271648', 'destination': '1988271616'}
        post_response = self.client.post(self.url, data, format='json')
        call_id = post_response.data['id']
        unique_call_url = self.url + str(call_id) + '/'
        response = self.client.get(unique_call_url, format='json')
        unique_call = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(unique_call['id'], call_id)

    def test_list_nonexistent_unique_call(self):

        call_id = 123
        unique_call_url = self.url + str(call_id) + '/'
        response = self.client.get(unique_call_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_call_with_different_numbers(self):

        data = {'source': '19988271648', 'destination': '19988271234'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_call_with_source_bigger_than_11(self):

        data = {'source': '19988271648123123', 'destination': '19988271234'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_call_with_destination_bigger_than_11(self):

        data = {'source': '19988271648', 'destination': '199882712311231214'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_call_with_same_numbers(self):

        data = {'source': '19988271648', 'destination': '19988271648'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_call_with_source_input_missing(self):

        data = {'source': '', 'destination': '19988271648'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_call_with_destination_input_missing(self):

        data = {'source': '19988271648', 'destination': ''}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_call_with_both_input_missing(self):

        data = {'source': '', 'destination': ''}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

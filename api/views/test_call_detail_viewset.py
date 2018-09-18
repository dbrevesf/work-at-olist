"""
Module containing the unit tests of the API endpoint Call
"""
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status


class CallDetailTest(APITestCase):
    """
    Class which contains the unit tests for the API endpoint: CallDetail
    """

    call_url = '/api/call/'
    url = '/api/calldetail/'
    client = APIClient()

    def test_list_call_details(self):

        call_data = {'source': '19988271648', 'destination': '1982312312'}
        call = self.client.post(self.call_url, call_data, format='json')
        call_details_data = {'call_id': call.data['id'],
                             'start': True,
                             'timestamp': '2018-09-14T01:16:54Z'}
        self.client.post(self.url, call_details_data, format='json')
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_unique_call_detail(self):

        call_data = {'source': '19988271648', 'destination': '1982312312'}
        call = self.client.post(self.call_url, call_data, format='json')
        call_details_data = {'call_id': call.data['id'],
                             'start': True,
                             'timestamp': '2018-09-14T01:16:54Z'}
        call_detail = self.client.post(self.url,
                                       call_details_data,
                                       format='json')
        unique_url = self.url + str(call_detail.data['id']) + '/'
        response = self.client.get(unique_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_nonexistent_unique_call_detail(self):

        unique_url = self.url + str(123) + '/'
        response = self.client.get(unique_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_empty_call_details(self):

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_call_detail(self):

        call_data = {'source': '19988271648', 'destination': '1982312312'}
        call = self.client.post(self.call_url, call_data, format='json')
        call_details_data = {'call_id': call.data['id'],
                             'start': True,
                             'timestamp': '2018-09-14T01:16:54Z'}
        response = self.client.post(self.url, call_details_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_without_call_id(self):

        call_details_data = {'call_id': '',
                             'start': True,
                             'timestamp': '2018-09-14T01:16:54Z'}
        response = self.client.post(self.url, call_details_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_with_nonexistent_call_id(self):

        call_data = {'source': '19988271648', 'destination': '1982312312'}
        self.client.post(self.call_url, call_data, format='json')
        call_details_data = {'call_id': '123123',
                             'start': True,
                             'timestamp': '2018-09-14T01:16:54Z'}
        response = self.client.post(self.url, call_details_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_without_start(self):

        call_data = {'source': '19988271648', 'destination': '1982312312'}
        call = self.client.post(self.call_url, call_data, format='json')
        call_details_data = {'call_id': call.data['id'],
                             'start': None,
                             'timestamp': '2018-09-14T01:16:54Z'}
        response = self.client.post(self.url, call_details_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_without_timestamp(self):

        call_data = {'source': '19988271648', 'destination': '1982312312'}
        call = self.client.post(self.call_url, call_data, format='json')
        call_details_data = {'call_id': call.data['id'],
                             'start': True,
                             'timestamp': ''}
        response = self.client.post(self.url, call_details_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_two_call_details_with_same_start_value(self):

        call_data = {'source': '19988271648', 'destination': '1982312312'}
        call = self.client.post(self.call_url, call_data, format='json')
        call_details_true = {'call_id': call.data['id'],
                             'start': True,
                             'timestamp': '2018-09-14T01:16:54Z'}
        self.client.post(self.url, call_details_true, format='json')
        call_details_false = {'call_id': call.data['id'],
                              'start': True,
                              'timestamp': '2018-09-14T01:18:54Z'}
        response_false = self.client.post(self.url,
                                          call_details_false,
                                          format='json')
        self.assertEqual(response_false.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_create_two_call_details_with_same_timestamp_value(self):

        call_data = {'source': '19988271648', 'destination': '1982312312'}
        call = self.client.post(self.call_url, call_data, format='json')
        call_details_true = {'call_id': call.data['id'],
                             'start': True,
                             'timestamp': '2018-09-14T01:16:54Z',
                             'teste': 'teste'}
        self.client.post(self.url, call_details_true, format='json')
        call_details_false = {'call_id': call.data['id'],
                              'start': False,
                              'timestamp': '2018-09-14T01:16:54Z',
                              'teste': 'teste'}
        response_false = self.client.post(self.url,
                                          call_details_false,
                                          format='json')
        self.assertEqual(response_false.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_create_call_detail_with_start_later_than_end(self):

        call_data = {'source': '19988271648', 'destination': '1982312312'}
        call = self.client.post(self.call_url, call_data, format='json')
        call_details_true = {'call_id': call.data['id'],
                             'start': True,
                             'timestamp': '2018-09-14T01:16:54Z'}
        call_details_false = {'call_id': call.data['id'],
                              'start': False,
                              'timestamp': '2018-08-14T01:16:54Z'}
        self.client.post(self.url, call_details_true, format='json')
        response_false = self.client.post(self.url,
                                          call_details_false,
                                          format='json')
        self.assertEqual(response_false.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_update_call_detail(self):

        call_data = {'source': '19988271648', 'destination': '1982312312'}
        call = self.client.post(self.call_url, call_data, format='json')
        call_details_data = {'call_id': call.data['id'],
                             'start': True,
                             'timestamp': '2018-09-14T01:16:54Z'}
        response = self.client.post(self.url, call_details_data, format='json')
        call_detail_id = response.data['id']
        unique_call_detail_url = self.url + str(call_detail_id) + '/'
        call_details_data = {'call_id': call.data['id'],
                             'start': False,
                             'timestamp': '2018-10-14T01:16:54Z',
                             'pk': call_detail_id}

        put_response = self.client.put(unique_call_detail_url,
                                       call_details_data,
                                       format='json')
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)

    def test_update_without_call_id(self):

        call_data = {'source': '19988271648', 'destination': '1982312312'}
        call = self.client.post(self.call_url, call_data, format='json')
        call_details_data = {'call_id': call.data['id'],
                             'start': True,
                             'timestamp': '2018-09-14T01:16:54Z'}
        response = self.client.post(self.url, call_details_data, format='json')
        call_detail_id = response.data['id']
        unique_call_detail_url = self.url + str(call_detail_id) + '/'
        call_details_data = {'call_id': '',
                             'start': True,
                             'timestamp': '2018-10-14T01:16:54Z',
                             'pk': call_detail_id}
        put_response = self.client.put(unique_call_detail_url,
                                       call_details_data,
                                       format='json')
        self.assertEqual(put_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_without_start(self):

        call_data = {'source': '19988271648', 'destination': '1982312312'}
        call = self.client.post(self.call_url, call_data, format='json')
        call_details_data = {'call_id': call.data['id'],
                             'start': True,
                             'timestamp': '2018-09-14T01:16:54Z'}
        response = self.client.post(self.url, call_details_data, format='json')
        call_detail_id = response.data['id']
        unique_call_detail_url = self.url + str(call_detail_id) + '/'
        call_details_data = {'call_id': call.data['id'],
                             'start': None,
                             'timestamp': '2018-10-14T01:16:54Z',
                             'pk': call_detail_id}
        put_response = self.client.put(unique_call_detail_url,
                                       call_details_data,
                                       format='json')
        self.assertEqual(put_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_without_timestamp(self):

        call_data = {'source': '19988271648', 'destination': '1982312312'}
        call = self.client.post(self.call_url, call_data, format='json')
        call_details_data = {'call_id': call.data['id'],
                             'start': True,
                             'timestamp': '2018-09-14T01:16:54Z'}
        response = self.client.post(self.url, call_details_data, format='json')
        call_detail_id = response.data['id']
        unique_call_detail_url = self.url + str(call_detail_id) + '/'
        call_details_data = {'call_id': call.data['id'],
                             'start': True,
                             'timestamp': '',
                             'pk': call_detail_id}
        put_response = self.client.put(unique_call_detail_url,
                                       call_details_data,
                                       format='json')
        self.assertEqual(put_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_with_timestamp_out_of_pattern(self):

        call_data = {'source': '19988271648', 'destination': '1982312312'}
        call = self.client.post(self.call_url, call_data, format='json')
        call_details_data = {'call_id': call.data['id'],
                             'start': True,
                             'timestamp': '2018-09-14T01:16:54Z'}
        response = self.client.post(self.url, call_details_data, format='json')
        call_detail_id = response.data['id']
        unique_call_detail_url = self.url + str(call_detail_id) + '/'
        call_details_data = {'call_id': call.data['id'],
                             'start': True,
                             'timestamp': '',
                             'pk': call_detail_id}
        put_response = self.client.put(unique_call_detail_url,
                                       call_details_data,
                                       format='json')
        self.assertEqual(put_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_two_call_details_with_same_start_value(self):

        call_data = {'source': '19988271648', 'destination': '1982312312'}
        call = self.client.post(self.call_url, call_data, format='json')
        call_details_data = {'call_id': call.data['id'],
                             'start': True,
                             'timestamp': '2018-09-14T01:16:54Z'}
        self.client.post(self.url, call_details_data, format='json')
        call_details_data = {'call_id': call.data['id'],
                             'start': False,
                             'timestamp': '2018-09-14T02:16:54Z'}
        response = self.client.post(self.url, call_details_data, format='json')

        call_detail_id = response.data['id']
        unique_call_detail_url = self.url + str(call_detail_id) + '/'
        call_details_data = {'start': True}
        put_response = self.client.put(unique_call_detail_url,
                                       call_details_data,
                                       format='json')
        self.assertEqual(put_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_call_detail_with_start_later_than_end(self):

        call_data = {'source': '19988271648', 'destination': '1982312312'}
        call = self.client.post(self.call_url, call_data, format='json')
        call_details_data = {'call_id': call.data['id'],
                             'start': True,
                             'timestamp': '2018-09-14T01:16:54Z'}
        response = self.client.post(self.url, call_details_data, format='json')
        call_details_data = {'call_id': call.data['id'],
                             'start': False,
                             'timestamp': '2018-09-14T02:16:54Z'}
        self.client.post(self.url, call_details_data, format='json')

        call_detail_id = response.data['id']
        unique_call_detail_url = self.url + str(call_detail_id) + '/'
        call_details_data = {'timestamp': '2018-09-14T03:16:54Z'}
        put_response = self.client.put(unique_call_detail_url,
                                       call_details_data,
                                       format='json')
        self.assertEqual(put_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_call_detail(self):

        call_data = {'source': '19988271648', 'destination': '1982312312'}
        call = self.client.post(self.call_url, call_data, format='json')
        call_details_data = {'call_id': call.data['id'],
                             'start': True,
                             'timestamp': '2018-09-14T01:16:54Z'}
        response = self.client.post(self.url, call_details_data, format='json')
        call_detail_id = response.data['id']
        unique_call_url = self.url + str(call_detail_id) + '/'
        delete_response = self.client.delete(unique_call_url, format='json')
        self.assertEqual(delete_response.status_code,
                         status.HTTP_204_NO_CONTENT)

    def test_delete_nonexistent_call_detail(self):

        unique_call_url = self.url + str(123) + '/'
        delete_response = self.client.delete(unique_call_url, format='json')
        self.assertEqual(delete_response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_create_more_than_two_call_details_for_a_single_call(self):

        call_data = {'source': '19988271648', 'destination': '1982312312'}
        call = self.client.post(self.call_url, call_data, format='json')
        call_details_data = {'call_id': call.data['id'],
                             'start': True,
                             'timestamp': '2018-09-14T01:16:54Z'}
        self.client.post(self.url, call_details_data, format='json')
        call_details_data = {'call_id': call.data['id'],
                             'start': False,
                             'timestamp': '2018-09-14T01:17:54Z'}
        self.client.post(self.url, call_details_data, format='json')

        call_details_data = {'call_id': call.data['id'],
                             'start': True,
                             'timestamp': '2018-09-14T01:18:54Z'}
        response = self.client.post(self.url, call_details_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

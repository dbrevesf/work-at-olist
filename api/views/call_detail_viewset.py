from api.models import CallDetail
from api.serializers import CallDetailSerializer
from api.utils import standardize_date
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

DATE_PATTERN = '%Y-%m-%dT%H:%M:%SZ'


class CallDetailViewSet(viewsets.ModelViewSet):
    """
    API endpoint to CallDetail
    """
    queryset = CallDetail.objects.all()
    serializer_class = CallDetailSerializer

    def __validate_input(self, request_data):
        """
        Method to validate the inputs for the API endpoint CallDetails.

        Parameters:

            request_data (Dictonary): Request data sent by the HTTP request

        Return:

            validation (Dictionary): Dictionary with error/success message.
        """
        call_id = request_data.get('call_id')
        request_timestamp = request_data.get('timestamp')
        request_start = request_data.get('start')
        validation = None
        if call_id and request_timestamp and request_start is not None:
            call_detail_query = CallDetail.objects.filter(call_id=call_id)
            if call_detail_query:
                if len(call_detail_query) < 2:
                    stored_call_detail = call_detail_query[0]
                    if isinstance(request_start, str):
                        if request_start in ['true', 'True']:
                            request_start = True
                        else:
                            request_start = False
                    if stored_call_detail.start == request_start:
                        validation = {'input_error':
                                      'a call must start and must end'}
                    stored_timestamp = standardize_date(
                        stored_call_detail.timestamp, DATE_PATTERN)
                    request_timestamp = standardize_date(request_timestamp,
                                                         DATE_PATTERN)
                    if stored_timestamp == request_timestamp:
                        validation = {'input_error':
                                      'the timestamps must be different'}
                    if stored_call_detail.start and not request_start:
                        if stored_timestamp > request_timestamp:
                            validation = {'input_error':
                                          'the end must be later'}
                    elif not stored_call_detail.start and request_start:
                        if stored_timestamp < request_timestamp:
                            validation = {'input_error':
                                          'the end must be later'}
                else:
                    validation = {'input_error':
                                  'limit of call details exceeded.'}

        return validation

    def create(self, request):

        response = None
        validation = self.__validate_input(request.data)
        if validation:
            response = Response(validation, status.HTTP_400_BAD_REQUEST)
        else:
            response = super(CallDetailViewSet, self).create(request)

        return response

    def update(self, request, pk=None):

        response = None
        validation = self.__validate_input(request.data)
        if validation:
            response = Response(validation, status.HTTP_400_BAD_REQUEST)
        else:
            response = super(CallDetailViewSet, self).update(request, pk)

        return response

from api import strings
from api.models import CallDetail
from api.serializers import CallDetailSerializer
from api.utils import standardize_date
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

CALL_DETAILS_LIMIT = 2


class CallDetailViewSet(viewsets.ModelViewSet):
    """
    API endpoint to CallDetail
    """
    queryset = CallDetail.objects.all()
    serializer_class = CallDetailSerializer

    def __validate_input(self, request_data):
        """
        Validate the inputs for the API endpoint CallDetails.

        Parameters:

            request_data (Dictonary): Request data sent by the HTTP request

        Return:

            validation (Dictionary): Dictionary with error/success message.
        """
        call_id = request_data.get(strings.CALL_ID_KEY)
        request_timestamp = request_data.get(strings.TIMESTAMP_KEY)
        request_start = request_data.get(strings.START_KEY)
        validation = None
        if call_id and request_timestamp and request_start is not None:
            call_detail_query = CallDetail.objects.filter(call_id=call_id)
            if call_detail_query:
                if len(call_detail_query) < CALL_DETAILS_LIMIT:
                    stored_call_detail = call_detail_query[0]
                    if isinstance(request_start, str):
                        if request_start in strings.TRUE_VALUES:
                            request_start = True
                        else:
                            request_start = False
                    if stored_call_detail.start == request_start:
                        validation = {strings.INPUT_ERROR_KEY:
                                      strings.START_END_ERROR}
                    stored_timestamp = standardize_date(
                        stored_call_detail.timestamp,
                        strings.COMPLETE_DATE_PATTERN)
                    request_timestamp = standardize_date(request_timestamp,
                                                         strings.
                                                         COMPLETE_DATE_PATTERN)
                    if stored_timestamp == request_timestamp:
                        validation = {strings.INPUT_ERROR_KEY:
                                      strings.EQUAL_TIMESTAMPS_ERROR}
                    if stored_call_detail.start and not request_start:
                        if stored_timestamp > request_timestamp:
                            validation = {strings.INPUT_ERROR_KEY:
                                          strings.SOONER_END_ERROR}
                    elif not stored_call_detail.start and request_start:
                        if stored_timestamp < request_timestamp:
                            validation = {strings.INPUT_ERROR_KEY:
                                          strings.SOONER_END_ERROR}
                else:
                    validation = {strings.INPUT_ERROR_KEY:
                                  strings.CALL_LIMIT_ERROR}

        return validation

    def create(self, request):
        """
        POST /api/calldetail
        """
        response = None
        validation = self.__validate_input(request.data)
        if validation:
            response = Response(validation, status.HTTP_400_BAD_REQUEST)
        else:
            response = super(CallDetailViewSet, self).create(request)

        return response

    def update(self, request, pk=None):
        """
        PUT /api/calldetail/<pk>
        """
        response = None
        validation = self.__validate_input(request.data)
        if validation:
            response = Response(validation, status.HTTP_400_BAD_REQUEST)
        else:
            response = super(CallDetailViewSet, self).update(request, pk)

        return response

from api import strings
from api.models import Call
from api.serializers import CallSerializer
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response


class CallViewSet(viewsets.ModelViewSet):
    """
    API endpoint to Call.
    """
    queryset = Call.objects.all()
    serializer_class = CallSerializer

    def __validate_input(self, request_data):
        """
        Validate the inputs for the API endpoint Call.

        Parameers:
            request_data (dictonary): Request data sent by the HTTP request

        Return:
            content (dictionary): Dictionary with error/success message.
        """
        content = None
        source = request_data.get(strings.SOURCE_KEY)
        destination = request_data.get(strings.DESTINATION_KEY)
        if source and destination:
            if source == destination:
                content = {strings.INPUT_ERROR_KEY:
                           strings.SOURCE_EQUAL_DESTINATION_ERROR}
            else:
                content = {strings.SUCCESS_KEY: strings.SUCCESS_KEY}
        else:
            content = {strings.INPUT_ERROR_KEY:
                       strings.SOURCE_OR_DESTINATION_MISSED_ERROR}
        return content

    def create(self, request):
        """
        POST /api/call
        """
        response = None
        validation = self.__validate_input(request.data)
        if strings.SUCCESS_KEY in validation:
            response = super(CallViewSet, self).create(request)
        else:
            response = Response(validation, status.HTTP_400_BAD_REQUEST)

        return response

    def update(self, request, pk=None):
        """
        PUT /api/call/<pk>/
        """
        response = None
        validation = self.__validate_input(request.data)
        if strings.SUCCESS_KEY in validation:
            response = super(CallViewSet, self).update(request, pk)
        else:
            response = Response(validation, status.HTTP_400_BAD_REQUEST)

        return response

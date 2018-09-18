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

    def validate_input(self, request_data):
        """
        Method to validate the inputs for the API endpoint Call.

        Parameters:

            request_data (Dictonary): Request data sent by the HTTP request

        Return:

            content (Dictionary): Dictionary with error/success message.
        """
        content = None
        source = request_data.get('source')
        destination = request_data.get('destination')
        if source and destination:
            if source == destination:
                content = {'input_error':
                           'source and destination must be different numbers'}
            else:
                content = {'success': 'success'}
        else:
            content = {'input_error':
                       'source and/or destination are missed'}
        return content

    def create(self, request):

        response = None
        validation = self.validate_input(request.data)
        if 'success' in validation:
            response = super(CallViewSet, self).create(request)
        else:
            response = Response(validation, status.HTTP_400_BAD_REQUEST)

        return response

    def update(self, request, pk=None):

        response = None
        validation = self.validate_input(request.data)
        if 'success' in validation:
            response = super(CallViewSet, self).update(request, pk)
        else:
            response = Response(validation, status.HTTP_400_BAD_REQUEST)

        return response

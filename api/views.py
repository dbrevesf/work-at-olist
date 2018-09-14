
from .models import Call
from .models import CallDetail
from .serializers import CallSerializer
from .serializers import CallDetailSerializer
from .utils import standardize_date
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
        if 'source' in request_data and 'destination' in request_data:
            # avoid calls with the same number for source and destination
            if request_data['source'] == request_data['destination']:
                content = {'input_error':
                           'source and destination must be different numbers'}
            else:
                # if everything's good, create the call
                content = {'success': 'success'}
        # source and destination is required to create a call
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


class CallDetailViewSet(viewsets.ModelViewSet):
    """
    API endpoint to CallDetail
    """
    queryset = CallDetail.objects.all()
    serializer_class = CallDetailSerializer

    def validate_input(self, request_data):
        """
        Method to validate the inputs for the API endpoint CallDetails.

        Parameters:

            request_data (Dictonary): Request data sent by the HTTP request

        Return:

            content (Dictionary): Dictionary with error/success message.
        """
        call_id = request_data.get('call_id')
        request_timestamp = request_data.get('timestamp')
        request_start = request_data.get('start')
        validation = None
        if call_id and request_timestamp and request_start is not None:
            call_detail_query = CallDetail.objects.filter(call_id=call_id)
            if call_detail_query:
                stored_call_detail = call_detail_query[0]

                # a call must have a start and an end.
                if stored_call_detail.start == request_start:
                    validation = {'input_error':
                                  'a call must start and must end'}

                # the timestamps must be different
                stored_timestamp = standardize_date(
                    stored_call_detail.timestamp)
                request_timestamp = standardize_date(request_timestamp)
                if stored_timestamp == request_timestamp:
                    validation = {'input_error':
                                  'the timestamps must be different'}

                # end time must be greater than start time
                if stored_call_detail.start and not request_start:
                    if stored_timestamp > request_timestamp:
                        validation = {'input_error': 'the end must be later'}
                elif not stored_call_detail.start and request_start:
                    if stored_timestamp < request_timestamp:
                        validation = {'input_error': 'the end must be later'}

        return validation

    def create(self, request):

        response = None
        validation = self.validate_input(request.data)
        if validation:
            response = Response(validation, status.HTTP_400_BAD_REQUEST)
        else:
            response = super(CallDetailViewSet, self).create(request)

        return response

    def update(self, request, pk=None):

        response = None
        validation = self.validate_input(request.data)
        if validation:
            response = Response(validation, status.HTTP_400_BAD_REQUEST)
        else:
            response = super(CallDetailViewSet, self).update(request, pk)

        return response

























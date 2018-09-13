from .models import Call
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .serializers import CallSerializer


class CallViewSet(viewsets.ModelViewSet):
    """
    API endpoint to fech Calls.
    """
    queryset = Call.objects.all()
    serializer_class = CallSerializer

    def create(self, request):

        response = None
        if 'source' in request.data and 'destination' in request.data:
            # avoid calls with the same number for source and destination
            if request.data['source'] == request.data['destination']:
                content = {'input error':
                           'source and destination must be different numbers'}
                response = Response(content, status.HTTP_400_BAD_REQUEST)
            else:
                # if everything's good, create the call
                response = super(CallViewSet, self).create(request)
        # source and destination is required to create a call
        else:
            content = {'input error':
                       'source and/or destination are missed'}
            response = Response(content, status.HTTP_400_BAD_REQUEST)

        return response

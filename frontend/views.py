from django.shortcuts import render
from api.views.telephone_bill_viewset import TelephoneBillViewSet
from rest_framework.views import APIView
from api import strings


# Create your views here.
def index(request):

    context = {}
    if request.GET:
        source = request.GET.get(strings.SOURCE_KEY)
        period = request.GET.get(strings.PERIOD_KEY)
        request = APIView().initialize_request(request)
        telephone_bill_viewset = TelephoneBillViewSet()
        response = telephone_bill_viewset.list(request)
        context = {strings.RESPONSE_KEY: response.data,
                   strings.SOURCE_KEY: source,
                   strings.PERIOD_KEY: period}
    return render(request, 'index.html', context)

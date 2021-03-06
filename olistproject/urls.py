"""olistproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.views.call_viewset import CallViewSet
from api.views.call_detail_viewset import CallDetailViewSet
from api.views.price_rule_viewset import PriceRuleViewSet
from api.views.price_rule_detail_viewset import PriceRuleDetailViewSet
from api.views.telephone_bill_viewset import TelephoneBillViewSet

router = routers.DefaultRouter()
router.register(r'call', CallViewSet)
router.register(r'calldetail', CallDetailViewSet)
router.register(r'pricerule', PriceRuleViewSet)
router.register(r'priceruledetail', PriceRuleDetailViewSet)
router.register(r'telephonebill',
                TelephoneBillViewSet,
                base_name='telephonebill')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('frontend.urls'))
]

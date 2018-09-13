from django.contrib import admin
from .models import Call, CallDetail, PriceRule, PriceRuleDetail

# Register your models here.
admin.site.register(Call)
admin.site.register(CallDetail)
admin.site.register(PriceRule)
admin.site.register(PriceRuleDetail)

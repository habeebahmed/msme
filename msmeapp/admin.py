from django.contrib import admin
from .models import Financials,Assets,Capital,Liabilities,Cash_Flows,Reserves,Application_Details, Business_Details,Applicant_Details
# Register your models here.
admin.site.register(Financials)
admin.site.register(Assets)
admin.site.register(Capital)
admin.site.register(Liabilities)
admin.site.register(Cash_Flows)
admin.site.register(Reserves)
admin.site.register(Application_Details)
admin.site.register(Business_Details)
admin.site.register(Applicant_Details)

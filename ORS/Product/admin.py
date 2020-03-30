from django.contrib import admin

# Register your models here.
from Product.models import *

admin.site.register(MachineReports)
admin.site.register(ReportAds)
admin.site.register(ReportMasterCategory)
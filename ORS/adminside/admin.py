from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Employee)
admin.site.register(CountryMaster)
admin.site.register(Statemaster)
admin.site.register(Citymaster)
admin.site.register(Workers)
admin.site.register(Brandmaster)


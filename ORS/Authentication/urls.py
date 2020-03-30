from django.urls import path
from .views import *

urlpatterns =[
    path('ajax/validate_username_login/', validate_username_login, name="validate_username_login"),
    path('ajax/validate_username_register/', validate_username_register, name="validate_username_register"),
    path('ajax/email-validate-forget-password',validate_forget_password_email,name="email-validate-forget-password"),
    path('ajax/Country',get_Country,name="Country"),
    path('ajax/State/',get_State,name="State"),
    path('ajax/City',get_City,name="City"),


]
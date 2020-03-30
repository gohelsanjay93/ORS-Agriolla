from django.urls import path
from .views import *
app_name = "Worker"
urlpatterns =[
    path("login/", Worker_login, name="worker"),
    path("ajax/validate_emp_username_login", validate_worker_username_login, name="validate_worker_username_login"),
    path("index/",index,name="index"),
    path("logout/",logout,name="logout"),
    path("index/addetails/<int:id>",addetails,name="addetails"),
    path("index/addetails/report",savereport,name="report"),

]
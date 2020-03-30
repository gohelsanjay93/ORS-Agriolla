from django.urls import path
from .views import *
app_name = "Emp"
urlpatterns =[
    path("emplogin/", emplogin, name="emplogin"),
    path("ajax/validate_emp_username_login", validate_emp_username_login, name="validate_emp_username_login"),
    path("",choice,name="choice"),
    path("index/",index,name="index"),
    path("index/users",tablesuser,name="users"),
    # path("index/ads",ads,name="ads"),
    path("index/postrequest",tables,name="postreq"),
    path("logout/",logout,name="logout"),
    path("index/postrequest/view/<int:id>",view,name="view"),
    path("index/postrequest/approval/<int:id>",verified,name="verify"),
    path("index/postrequest/reject/<int:id>",reject,name="reject"),
    path("index/postrequest/visitdate",visitdate,name="visit"),
    path("ajax/reportsave",SaveMachineReports,name="reportsave")
]
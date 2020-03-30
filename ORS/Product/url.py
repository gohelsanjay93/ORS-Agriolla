from django.urls import path
from .views import *
app_name="Product"
urlpatterns = [
 path('categoryproduct/<int:cid>',categoryproduct,name="categorizedproduct"),
 path('viewallads/',viewallads,name="allads"),
 path('viewallads/details/<int:pk>',addetails,name="addetails"),
 path('search/',searchedad,name="searchad")
]
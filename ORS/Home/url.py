from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from .views import *

app_name = "Home"
urlpatterns =[
    path('', home, name="home"),
    path('product/addproduct',addproduct,name="addproduct"),
    path('aboutus',aboutus,name="aboutus"),
    path('contactus',contactus,name="contactus"),
    path('product/editproduct/<int:pk>',editproduct,name="editproduct"),
    path('product/delete/<int:pk>',deleteproduct,name="deleteproduct"),
    path('dashboard/',dashboard,name="dashboard"),
    path('dashboard/Editprofile', profile, name="editprofile"),
    path('dashboard/save', saveprofile, name="saveprofile"),
    path('dashboard/activead',activead,name="activead"),
    path('dashboard/pending',pending,name="pendingad"),
    path('dashboard/aboutme',aboutme,name="aboutme"),
    path('alter/Register',AfterRegistration,name="sr"),
    path('product/details/payment/<int:id>',paymentform,name="payment"),
    path('product/details/payment/',paymentdone,name="paymentdone")
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
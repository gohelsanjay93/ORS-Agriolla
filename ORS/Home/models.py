import os
import random

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save

from ORS.utils.utils import *

from adminside.models import *

from adminside.models import CountryMaster, Citymaster

BooleanChoice = (
    (True, "Yes"),
    (False, "No")
)



# def get_filename_ext(filepath):
#     base_name=os.path.basename(filepath)
#     name, ext=get_filename_ext(filepath
#     return name,ext
#
# def upload_image_path(instance,filename):
#     new_filename = random.randint(1, 1000)
#     name, ext = get_filename_ext(filename)
#     final_filename='(new_filename)(ext)'.format(new_filename=new_filename, ext=ext)
#     return "users/(final_filename)".format(final_filename=final_filename)

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 1000)  # this will generate new files' name
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return final_filename


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13)
    address = models.TextField(null=False)
    pincode = models.CharField(max_length=6, null=False)
    country = models.ForeignKey(CountryMaster, on_delete=models.CASCADE, null=True, blank=True)
    state = models.ForeignKey(Statemaster, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(Citymaster, on_delete=models.CASCADE, null=True, blank=True)
    Birthdate = models.DateField(null=True,blank=True)
    IsActive = models.BooleanField(choices=BooleanChoice, default=False)
    IsAvailable = models.BooleanField(choices=BooleanChoice,default=False)
    created_on = models.DateTimeField(auto_now=True,null=True,blank=True)
    updated_on = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    IsMerchant = models.BooleanField(default=False, choices=BooleanChoice)
    # Role = models.ForeignKey(Roles,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.user.username

class Shops(models.Model):
    ShopOwner = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    ShopName = models.CharField(max_length=100)
    ShopImage = models.ImageField(null=True,blank=True)
    ShopAddress = models.TextField(null=False)
    ShopCountry = models.ForeignKey(CountryMaster, on_delete=models.CASCADE,null=True,blank=True)
    ShopState = models.ForeignKey(Statemaster, on_delete=models.CASCADE,null=True,blank=True)
    ShopCity = models.ForeignKey(Citymaster, on_delete=models.CASCADE,null=True,blank=True)
    PostCode = models.CharField(max_length=6, null=False,blank=False)
    IsVerifiedSeller = models.BooleanField(choices=BooleanChoice, default=False)
    IsActive = models.BooleanField(choices=BooleanChoice)

    def __str__(self):
        return str(self.ShopOwner)

class contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=50)
    message = models.TextField(default='')

    def __str__(self):
        return self.name


AD_CHOICES = (
    ('Sell', 'Sell'),
    ('Rent', 'Rent')
)
verifystatus = (
    ('yes', 'yes'),
    ('no', 'no')
)
Reject = (
    ('yes', 'yes'),
    ('no', 'no')
)
GREATAD_CHOICES = (
    ('yes', 'yes'),
    ('no', 'no')
)
OFFER_CHOICES = (
    ('yes', 'yes'),
    ('no', 'no')
)
AVAILABLE_CHOICES = (
    ('Available', 'Available'),
    ('!Available', '!Available')
)
QUANTITY_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)

Condition =(
    ('New', 'New'),
    ('Old', 'Old')
)
class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    slug = models.SlugField(blank=True, unique=True)
    Owner_name = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True)
    uploadfor = models.CharField(max_length=5, choices=AD_CHOICES, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brandmaster,on_delete=models.CASCADE, blank=True, null=True)
    Description = models.TextField(null=True, blank=True)
    Feature1 = models.CharField(max_length=50, null=False, blank=False,default="")
    Feature2 = models.CharField(max_length=50, null=True, blank=True,default="")
    Feature3 = models.CharField(max_length=50, null=True, blank=True,default="")
    Feature4 = models.CharField(max_length=50, null=True, blank=True,default="")
    Feature5 = models.CharField(max_length=50, null=True, blank=True,default="")
    Condition = models.CharField(max_length=5,choices=Condition,null=True,blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    quantity = models.CharField(max_length=2, choices=QUANTITY_CHOICES, blank=True, null=True)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    image2 = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    image3 = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    image4 = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    image5 = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    avail = models.CharField(max_length=10, choices=AVAILABLE_CHOICES, default="!Available")
    advalue = models.CharField(default="no", max_length=10, choices=GREATAD_CHOICES, blank=True, null=True)
    offer = models.CharField(default="no", max_length=5, choices=OFFER_CHOICES, blank=True, null=True)
    offerDetails = models.CharField(max_length=50,default="")
    adviewed = models.IntegerField(default=0, blank=True, null=True)
    rejected_status = models.CharField(max_length=5, choices=Reject, default="no")
    rejection_reason = models.CharField(max_length=100,null=True,blank=True)
    verified_status = models.CharField(max_length=5, default="no")
    visit_date = models.DateTimeField(null=True, blank=True)
    verifier_person = models.ForeignKey(Workers,on_delete=models.CASCADE, null=True, blank=True)
    ApprovedOrRejectedBy = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True)
    IsVisited = models.BooleanField(default=False,choices=BooleanChoice)
    IsReported = models.BooleanField(default=False,choices=BooleanChoice)
    Rate = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    post_date = models.DateTimeField(auto_now=True,null=True)
    update_date = models.DateTimeField(auto_now_add=True,null=True)
    IsProductSoldOrOnRent=models.BooleanField(choices=BooleanChoice,default=False)

    def __str__(self):
        return self.title

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)

class Payment(models.Model):
    transactionid = models.CharField(unique=True,max_length=100,null=True,blank=True)
    Merchant = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    PaymentType= models.CharField(max_length=50,null=True,blank=True)
    Paymentfor = models.ForeignKey(Product,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9,decimal_places=2,null=True)
    Createddate = models.DateTimeField(auto_now=True,null=True)
    status = models.BooleanField(choices=BooleanChoice,default=False)

class Producttransaction(models.Model):
    productid = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    borrower = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    takendate = models.DateField(null=True,blank=True)
    returndte= models.DateField(null=True,blank=True)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# import os
# import random
#
# from django.contrib.auth.models import User
# from django.db import models
# from django.db.models import Model
# from django.db.models.signals import *
# from django.dispatch import receiver
#
# from django.contrib import messages
# from django.shortcuts import redirect, get_object_or_404
# from django.shortcuts import render
#
# # Create your models here.
# from ORS.utils.utils import *
#
# from adminside.models import Citymaster, CountryMaster, Statemaster
#
# GENDER_CHOICES = (
#     ('M', 'Male'),
#     ('F', 'Female'),
#     ('O', 'Other'),
# )
# BooleanChoice = (
#     (True, "Yes"),
#     (False, "No")
# )
# COUNTRY_CHOICES = (
#     ('India', 'India'),
# )
# City_CHOICES = (
#     ('Ahmedabad', 'Ahmedabad'),
#     ('Bagodara', 'Bagodara')
# )
# STATE_CHOICES = (
#     ('Gujarat', 'Gujarat'),
#     ('Maharashtra', 'Maharashtra')
# )
#
#
# # def get_filename_ext(filepath):
# #     base_name=os.path.basename(filepath)
# #     name, ext=get_filename_ext(filepath
# #     return name,ext
# #
# # def upload_image_path(instance,filename):
# #     new_filename = random.randint(1, 1000)
# #     name, ext = get_filename_ext(filename)
# #     final_filename='(new_filename)(ext)'.format(new_filename=new_filename, ext=ext)
# #     return "users/(final_filename)".format(final_filename=final_filename)
#
# def get_filename_ext(filepath):
#     base_name = os.path.basename(filepath)
#     name, ext = os.path.splitext(base_name)
#     return name, ext
#
#
# def upload_image_path(instance, filename):
#     new_filename = random.randint(1, 1000)  # this will generate new files' name
#     name, ext = get_filename_ext(filename)
#     final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
#     return final_filename
#
#
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     phone = models.CharField(max_length=13)
#     address = models.TextField(null=False)
#     pincode = models.CharField(max_length=6, null=False)
#     country = models.ForeignKey(CountryMaster, on_delete=models.CASCADE, null=True, blank=True)
#     state = models.ForeignKey(Statemaster, on_delete=models.CASCADE, null=True, blank=True)
#     city = models.ForeignKey(Citymaster, on_delete=models.CASCADE, null=True, blank=True)
#     age = models.CharField(max_length=2, null=False)
#     IsActive = models.BooleanField(BooleanChoice, default=False)
#     IsAvailable = models.BooleanField(BooleanChoice, default=False)
#     created_on = models.DateTimeField(auto_now=True)
#     updated_on = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.user
#
#     # class Profile(models.Model):
#     #     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     #     phone = models.CharField(max_length=13)
#     #     address = models.TextField(null=False)
#     #     pincode = models.CharField(max_length=6, null=False)
#     #     country = models.CharField(max_length=10, choices=COUNTRY_CHOICES)
#     #     state = models.CharField(max_length=10, null=False, choices=STATE_CHOICES)
#     #     city = models.CharField(max_length=20, choices=City_CHOICES, null=True, blank=True)
#     #     age = models.CharField(max_length=2, null=False)
#     #     created_on = models.DateTimeField(auto_now=True)
#     #     updated_on = models.DateTimeField(auto_now_add=True)
#     #
#     #     def __str__(self):
#     #         return self.user
#
#
# class contact(models.Model):
#     name = models.CharField(max_length=20)
#     email = models.EmailField(max_length=50)
#     subject = models.CharField(max_length=50)
#     message = models.TextField(default='')
#
#     def __str__(self):
#         return self.name
#
#
# # @receiver(post_save, sender=User)
# # def create_user_profile(sender, instance, created, **kwargs):
# #     if created:
# #         Profile.objects.create(user=instance)
# #
# #
# # @receiver(post_save, sender=User)
# # def save_user_profile(sender, instance, **kwargs):
# #     instance.profile.save()
#
#
# from django.db import models
#
# # Create your models here.
# from django.db.models.signals import pre_save
#
# AD_CHOICES = (
#     ('Sell', 'Sell'),
#     ('Rent', 'Rent')
# )
# verifystatus = (
#     ('yes', 'yes'),
#     ('no', 'no')
# )
# Reject = (
#     ('yes', 'yes'),
#     ('no', 'no')
# )
# GREATAD_CHOICES = (
#     ('yes', 'yes'),
#     ('no', 'no')
# )
# OFFER_CHOICES = (
#     ('yes', 'yes'),
#     ('no', 'no')
# )
# AVAILABLE_CHOICES = (
#     ('Available', 'Available'),
#     ('!Available', '!Available')
# )
# QUANTITY_CHOICES = (
#     ('1', '1'),
#     ('2', '2'),
#     ('3', '3'),
#     ('4', '4'),
#     ('5', '5'),
# )
#
#
# class Category(models.Model):
#     name = models.CharField(max_length=20)
#     slug = models.SlugField(blank=True, unique=True)
#
#     def __str__(self):
#         return self.name
#
#
# class Product(models.Model):
#     title = models.CharField(max_length=50, blank=True, null=True)
#     slug = models.SlugField(blank=True, unique=True)
#     Owner_name = models.CharField(max_length=50, blank=True, null=True)
#     uploadfor = models.CharField(max_length=5, choices=AD_CHOICES, blank=True, null=True)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     brand = models.CharField(max_length=30, blank=True, null=True)
#     Description = models.TextField(null=True, blank=True)
#     price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
#     quantity = models.CharField(max_length=2, choices=QUANTITY_CHOICES, blank=True, null=True)
#     image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
#     avail = models.CharField(max_length=10, choices=AVAILABLE_CHOICES, default="!Available")
#     rejected_status = models.CharField(max_length=5, choices=Reject, default="no")
#     advalue = models.CharField(default="no", max_length=10, choices=GREATAD_CHOICES, blank=True, null=True)
#     offer = models.CharField(default="no", max_length=5, choices=OFFER_CHOICES, blank=True, null=True)
#     post_date = models.DateTimeField(auto_now=True, blank=True, null=True)
#     update_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
#     adviewed = models.IntegerField(default=0, blank=True, null=True)
#     verified_status = models.CharField(max_length=5, default="no")
#     visit_date = models.DateTimeField(null=True, blank=True)
#     verifier_person = models.CharField(max_length=50, null=True, blank=True)
#
#     def __str__(self):
#         return self.title
#
#
# def product_pre_save_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)
#
#
# pre_save.connect(product_pre_save_receiver, sender=Product)
#
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++= ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#           |\  | !==== |    |
#           | \ | |==   | /\ |
#           |  \| !==== |/  \|
#
# import os
# import random
# from ORS.utils.utils import *
# from django.contrib.auth.models import User
# from django.db import models
# from django.db.models.signals import *
# # Create your models here.
#
# AD_CHOICES = (
#     ('Sell', 'Sell'),
#     ('Rent', 'Rent')
# )
#
# verifystatus = (
#     ('yes', 'yes'),
#     ('no', 'no')
# )
# Reject = (
#     ('yes', 'yes'),
#     ('no', 'no')
# )
# GREATAD_CHOICES = (
#     ('yes', 'yes'),
#     ('no', 'no')
# )
# OFFER_CHOICES = (
#     ('yes', 'yes'),
#     ('no', 'no')
# )
# AVAILABLE_CHOICES = (
#     ('Available', 'Available'),
#     ('!Available', '!Available')
# )
# QUANTITY_CHOICES = (
#     ('1', '1'),
#     ('2', '2'),
#     ('3', '3'),
#     ('4', '4'),
#     ('5', '5'),
# )
# CATEGORY_CHOICES = (
#     ('Machines', 'Machine'),
#     ('Chemicals', 'Chemical'),
#     ('Tools', 'Tool'),
# )
# GENDER_CHOICES = (
#     ('M', 'Male'),
#     ('F', 'Female'),
#     ('O', 'Other'),
# )
# BoolChoice = (
#     (True, 'yes'),
#     (False, 'no')
# )
# COUNTRY_CHOICES = (
#     ('India', 'India'),
# )
# City_CHOICES = (
#     ('Ahmedabad', 'Ahmedabad'),
#     ('Bagodara', 'Bagodara')
# )
# STATE_CHOICES = (
#     ('Gujarat', 'Gujarat'),
#     ('Maharashtra', 'Maharashtra')
# )
#
# def get_filename_ext(filepath):
#     base_name = os.path.basename(filepath)
#     name, ext = os.path.splitext(base_name)
#     return name, ext
#
#
# def upload_image_path(instance, filename):
#     new_filename = random.randint(1, 1000)  # this will generate new files' name
#     name, ext = get_filename_ext(filename)
#     final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
#     return final_filename
#
# class CountryMaster(models.Model):
#     CountryName = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.CountryName
#
# class Statemaster(models.Model):
#     StateName = models.CharField(max_length=50)
#     Country = models.ForeignKey(CountryMaster, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.StateName
#
# class Citymaster(models.Model):
#     CityName = models.CharField(max_length=50)
#     State = models.ForeignKey(Statemaster, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.CityName
#
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     phone = models.CharField(max_length=15)
#     address = models.TextField(null=False)
#     pincode = models.CharField(max_length=6, null=False)
#     country = models.ForeignKey(CountryMaster, on_delete=models.CASCADE)
#     state = models.ForeignKey(Statemaster, on_delete=models.CASCADE)
#     city = models.ForeignKey(Citymaster, on_delete=models.CASCADE)
#     DateofBirth = models.DateField(blank=True, null=True)
#     IsShopkeeper = models.BooleanField(choices=BoolChoice, default=False)
#     IsVerifiedSeller = models.BooleanField(choices=BoolChoice, default=False)
#     created_on = models.DateTimeField(auto_now=True)
#     updated_on = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.user
#
# # class Shops(models.Model):
# #     ShopOwner = models.ForeignKey(User,on_delete=models.CASCADE)
# #     ShopName = models.CharField(max_length=100)
# #     ShopImage = models.CharField(max_length=255)
# #     ShopAddress = models.TextField(null=False)
# #     ShopCountry = models.ForeignKey(CountryMaster, on_delete=models.CASCADE)
# #     ShopState = models.ForeignKey(Statemaster, on_delete=models.CASCADE)
# #     ShopCity = models.ForeignKey(Citymaster, on_delete=models.CASCADE)
# #     PostCode = models.CharField(max_length=6, null=False,blank=False)
# #     IsVerifiedSeller = models.BooleanField(choices=BoolChoice, default=False)
# #     IsActive = models.BooleanField(choices=BoolChoice)
# #
# #     def __str__(self):
# #         return self.ShopOwner
#
#
# class contact(models.Model):
#     name = models.CharField(max_length=20)
#     email = models.EmailField(max_length=50)
#     subject = models.CharField(max_length=50)
#     message = models.TextField(default='')
#
#     def __str__(self):
#         return self.name
#
# class Category(models.Model):
#     name = models.CharField(max_length=20)
#     slug = models.SlugField(blank=True, unique=True)
#
#     def __str__(self):
#         return self.name
#
#
# class Product(models.Model):
#     title = models.CharField(max_length=50, blank=True, null=True)
#     slug = models.SlugField(blank=True, unique=True)
#     Owner_name = models.CharField(max_length=50, blank=True, null=True)
#     uploadfor = models.CharField(max_length=5, choices=AD_CHOICES, blank=True, null=True)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     brand = models.CharField(max_length=30, blank=True, null=True)
#     Description = models.TextField(null=True, blank=True)
#     price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
#     quantity = models.CharField(max_length=1, choices=QUANTITY_CHOICES, blank=True, null=True)
#     image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
#     avail = models.CharField(max_length=10, choices=AVAILABLE_CHOICES, default="!Available")
#     rejected_status = models.CharField(max_length=5, choices=Reject, default="no")
#     advalue = models.CharField(default="no", max_length=10, choices=GREATAD_CHOICES, blank=True, null=True)
#     offer = models.CharField(default="no", max_length=5, choices=OFFER_CHOICES, blank=True, null=True)
#     post_date = models.DateTimeField(auto_now=True, blank=True, null=True)
#     update_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
#     adviewed = models.IntegerField(default=0, blank=True, null=True)
#     verified_status = models.CharField(max_length=5, default="no")
#     visit_date = models.DateTimeField(null=True, blank=True)
#     verifier_person = models.CharField(max_length=50, null=True, blank=True)
#
#     def __str__(self):
#         return self.title
#
#
# def product_pre_save_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)
#
#
# pre_save.connect(product_pre_save_receiver, sender=Product)
#
#
#
# # @receiver(post_save, sender=User)
# # def create_user_profile(sender, instance, created, **kwargs):
# #     if created:
# #         Profile.objects.create(user=instance)
# #
# #
# # @receiver(post_save, sender=User)
# # def save_user_profile(sender, instance, **kwargs):
# #     instance.profile.save()

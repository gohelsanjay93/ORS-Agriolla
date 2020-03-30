import os
import random

from django.db import models

Boolchoices = (
    (True, "Yes"),
    (False, "No")
)


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

# Create your models here.
class CountryMaster(models.Model):
    CountryName = models.CharField(max_length=50)

    def __str__(self):
        return self.CountryName


class Statemaster(models.Model):
    StateName = models.CharField(max_length=50)
    Country = models.ForeignKey(CountryMaster, on_delete=models.CASCADE)

    def __str__(self):
        return self.StateName


class Citymaster(models.Model):
    CityName = models.CharField(max_length=50)
    State = models.ForeignKey(Statemaster, on_delete=models.CASCADE)

    def __str__(self):
        return self.CityName


class Employee(models.Model):
    username = models.CharField(max_length=20, null=False, blank=False)
    firstname = models.CharField(max_length=20, null=False, blank=False)
    lastname = models.CharField(max_length=20, null=False, blank=False)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10, null=False)
    address = models.TextField()
    Postcode = models.CharField(max_length=6, null=True, blank=True)
    Country = models.ForeignKey(CountryMaster, on_delete=models.CASCADE, null=True, blank=True)
    State = models.ForeignKey(Statemaster, on_delete=models.CASCADE, null=True, blank=True)
    City = models.ForeignKey(Citymaster, on_delete=models.CASCADE, null=True, blank=True)
    dob = models.DateField(null=False, blank=False)
    password = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.firstname + "" + self.lastname


class Brandmaster(models.Model):
    BrandName = models.CharField(max_length=50)
    BrandUrl = models.CharField(max_length=255)
    BrandLogo = models.ImageField(null=True, blank=True)
    IsActive = models.BooleanField(choices=Boolchoices, default=False)

    def __str__(self):
        return self.BrandName

class Workers(models.Model):
    FirstName = models.CharField(max_length=50)
    Lastname = models.CharField(max_length=50)
    Username = models.CharField(max_length=50,unique=True)
    Password = models.CharField(max_length=50,null=True,blank=True)
    Email = models.EmailField(max_length=255, unique=True)
    Phone = models.CharField(max_length=15,unique=True)
    Address = models.TextField()
    Postcode = models.CharField(max_length=6, null=True, blank=True)
    Country = models.ForeignKey(CountryMaster, on_delete=models.CASCADE, null=True, blank=True)
    State = models.ForeignKey(Statemaster, on_delete=models.CASCADE, null=True, blank=True)
    City = models.ForeignKey(Citymaster, on_delete=models.CASCADE, null=True, blank=True)
    Birthdate = models.DateField(null=False, blank=False)
    IdProof = models.FileField(null=True, blank=True)
    AddressProof = models.FileField(null=True, blank=True)
    IsActive = models.BooleanField(choices=Boolchoices, default=False)
    IsAvailable = models.BooleanField(choices=Boolchoices, default=False)

    def __str__(self):
        return self.FirstName + " "+ self.Lastname

class Roles(models.Model):
    Rolename = models.CharField(max_length=50)
    Permissions = models.CharField(max_length=300)

    def __str__(self):
        return self.Rolename

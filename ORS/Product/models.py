from django.db import models
from Home.models import Product

Boolchoices = (
    (True, "Yes"),
    (False, "No")
)
OwnerN = (
    ('FirstOwner', "FirstOwner"),
    ('SecondOwner', "SecondOwner"),
    ('ThirdOwner', "ThirdOwner"),
)

class ReportMasterCategory(models.Model):
    Categoryname = models.CharField(max_length=50)
    IsActive = models.BooleanField(default=True, choices=Boolchoices)

    def __str__(self):
        return self.Categoryname

class ReportAds(models.Model):
    # from Home.models import Product
    ReportedAd = models.ForeignKey(Product, on_delete=models.CASCADE)
    ReportedBy = models.IntegerField()
    ReportCategory = models.ForeignKey(ReportMasterCategory, on_delete=models.CASCADE)
    ReportotherCategory = models.CharField(null=True, blank=True, max_length=50)
    ReportMessage = models.TextField()
    CreatedOn = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.ReportedAd)

class MachineReports(models.Model):
    Adid = models.OneToOneField(Product, on_delete=models.CASCADE)
    ManufaturedDate = models.DateField(null=True, blank=True)
    IdentificationNumber = models.CharField(max_length=100,null=True,blank=True)
    Engine = models.CharField(max_length=100,null=True,blank=True)
    Power = models.CharField(max_length=100, null=True, blank=True)
    Fuel = models.CharField(max_length=50, null=True, blank=True)
    WorkEfficiency = models.CharField(max_length=100, null=True, blank=True)
    IsWorking = models.BooleanField(choices=Boolchoices, default=True)
    WorkFor1 = models.CharField(max_length=50, null=False, blank=False)
    WorkFor2 = models.CharField(max_length=50, null=True, blank=True)
    WorkFor3 = models.CharField(max_length=50, null=True, blank=True)
    Extrainfo = models.TextField(null=True,blank=True)
    def __str__(self):
        return str(self.Adid)

# from django.db import models
#
# # Create your models here.
# from django.db.models.signals import pre_save
#
# AD_CHOICES =(
#     ('Sell','Sell'),
#     ('Rent','Rent')
# )
#
# GREATAD_CHOICES =(
#     ('yes','yes'),
#     ('no','no')
# )
# OFFER_CHOICES =(
#     ('yes','yes'),
#     ('no','no')
# )
# AVAILABLE_CHOICES =(
#     ('Available','Available'),
#     ('!Available','!Available')
# )
# QUANTITY_CHOICES = (
#     ('1','1'),
#     ('2','2'),
#     ('3','3'),
#     ('4','4'),
#     ('5','5'),
# )
# CATEGORY_CHOICES = (
#     ('Machines','Machine'),
#     ('Chemicals','Chemical'),
#     ('Tools','Tool'),
# )
# class Category(models.Model):
#     name = models.CharField(max_length=20)
#     slug = models.SlugField(blank=True,unique=True)
#
#     def __str__(self):
#         return self.name
#
# class Product(models.Model):
#     title = models.CharField(max_length=50,blank=True,null=True)
#     slug = models.SlugField(blank=True,unique=True)
#     Owner_name = models.CharField(max_length=50,blank=True,null=True)
#     uploadfor = models.CharField(max_length=5,choices=AD_CHOICES,blank=True,null=True)
#     category = models.ForeignKey(Category,on_delete=models.CASCADE)
#     brand = models.CharField(max_length=30,blank=True,null=True)
#     Description = models.TextField(null=True,blank=True)
#     price = models.DecimalField(max_digits=6,decimal_places=2,blank=True,null=True)
#     quantity = models.CharField(max_length=1,choices=QUANTITY_CHOICES,blank=True,null=True)
#     image = models.ImageField(null=True,blank=True)
#     avail = models.CharField(max_length=10,choices=AVAILABLE_CHOICES,blank=True,null=True)
#     advalue = models.CharField(default="no",max_length=10,choices=GREATAD_CHOICES,blank=True,null=True)
#     offer = models.CharField(default="no",max_length=5,choices=OFFER_CHOICES,blank=True,null=True)
#     post_date = models.DateTimeField(auto_now=True,blank=True,null=True)
#     update_date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
#     adviewed = models.IntegerField(default=0,blank=True,null=True)
#
#
#     def __str__(self):
#         return self.title
#
#
# def product_pre_save_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         from ORS.ORS.utils.utils import unique_slug_generator
#         instance.slug = unique_slug_generator(instance)
#
#
# pre_save.connect(product_pre_save_receiver, sender=Product)

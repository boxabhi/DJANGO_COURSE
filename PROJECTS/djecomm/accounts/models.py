from django.db import models
from django.contrib.auth.models import User



class Customer(User):
    profile_image = models.ImageField(upload_to="customer/", null=True , blank=True)



class Shopkeeper(User):
    gst_number = models.CharField(max_length=15)
    adhar_number = models.CharField(max_length=14)
    profile_image = models.ImageField(upload_to="customer/", null=True , blank=True)
    bmp_id = models.CharField(max_length=100, unique=True)
    vendor_name = models.CharField(max_length=100)





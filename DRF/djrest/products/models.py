from django.db import models

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = False)

class AdminObjectsManager()

class 

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_brand = models.CharField(max_length=100)
    product_price = models.FloatField()
    is_deleted = models.BooleanField(default=False)
    is_admin_objects = models.BooleanField()
    objects = SoftDeleteManager()
    all_objects = models.Manager()


class Student():
    is_deleted = models.BooleanField(default=False) 
    objects = SoftDeleteManager()
    all_objects = models.Manager()


Product.objects.filter()




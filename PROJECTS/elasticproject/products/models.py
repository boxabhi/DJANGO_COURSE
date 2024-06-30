from django.db import models

# Create your models here.

class Brand(models.Model):
    brand_name = models.CharField(max_length= 100)

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=100)
    price = models.FloatField()
    brand_name = models.ForeignKey(Brand , on_delete=models.CASCADE, null = True , blank=True)
    brand = models.CharField(max_length=100, null = True , blank=True)
    sku = models.CharField(max_length=100)
    thumbnail = models.URLField(max_length=1000)
   

    def __str__(self) -> str:
        return self.title
from django.db import models


class Tags(models.Model):
    tag = models.CharField(max_length=100)

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=100)
    price = models.FloatField()
    brand = models.CharField(max_length=100, null = True , blank=True)
    sku = models.CharField(max_length=100)
    thumbnail = models.URLField(max_length=1000)
    tags = models.ManyToManyField(Tags)


    def __str__(self) -> str:
        return self.title
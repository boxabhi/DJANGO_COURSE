from django.db import models
from django.contrib.auth.models import User


class Store(models.Model):
    bmp_id = models.CharField(unique=True , max_length=100)
    store_name = models.CharField(max_length=100)
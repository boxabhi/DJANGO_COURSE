from django.db import models

# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField()
    image = models.URLField()
    external_link = models.URLField()
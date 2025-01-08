from django.db import models

# Create your models here.

class Student(models.Model):
    student_id = models.CharField(max_length=100,null=True , blank=True)
    name = models.CharField(max_length=100, db_index=True)
    dob = models.DateField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=100)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]
    


class Author(models.Model):
    name = models.CharField(max_length=100, null=True ,blank=True)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField()
    
    def __str__(self):
        return self.name



class Book(models.Model):
    book_title = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(Author,on_delete=models.CASCADE, null=True , blank=True)
    publishers = models.ManyToManyField(Publisher, related_name="books")

    class Meta:
        default_related_name = "author_books"


    def __str__(self):
        return self.book_title

def send_email():
    print("Email sent")

from django.db.models.signals import post_save
from django.dispatch import receiver
    


import uuid


def generateSlug():
    return str(uuid.uuid4())

class Product(models.Model):
    name = models.CharField(max_length=100)
    product_slug = models.SlugField(unique=True, default=generateSlug)
    description = models.TextField()
    price = models.FloatField()
    in_stock = models.BooleanField(default=True)


    class Meta:
        indexes = [

            models.Index(fields=['in_stock'], name='product_in_stock_idx', condition=models.Q(in_stock=True)),
        ]





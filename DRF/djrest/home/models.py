from django.db import models

# Create your models here.

class Student(models.Model):
    student_id = models.CharField(max_length=100,null=True , blank=True)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=100)
    


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField()
    
    def __str__(self):
        return self.name



class Book(models.Model):
    book_title = models.CharField(max_length=100, unique=True)
    author = models.ForeignKey(Author,on_delete=models.CASCADE, related_name="book_publisher", null=True , blank=True)
    publishers = models.ManyToManyField(Publisher, related_name="books")



    def __str__(self):
        return self.book_title

    


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
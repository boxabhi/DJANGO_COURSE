from typing import Iterable
from django.db import models
from home.utils import generateSlug



class College(models.Model):
    college_name = models.CharField(max_length=100)
    college_address = models.CharField(max_length=100)

class Student(models.Model):
    gender_choices = (('Male', 'Male') , ('Female' , 'Female'))
    college = models.ForeignKey(College, on_delete=models.CASCADE , null =True , blank=True)
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=12)
    email = models.EmailField()
    gender = models.CharField(max_length=10 ,choices=gender_choices , default = "Male")
    age = models.IntegerField(null = True , blank=True)
    student_bio = models.TextField()



class Author(models.Model):
    author_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.author_name 

class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=100)
    published_date = models.DateField(null=True , blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Brand(models.Model):
    brand_name = models.CharField(max_length=100)
    country = models.CharField(default="IN",max_length=100)

    def __str__(self):
        return self.brand_name

class Products(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True , blank = True)
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=True , blank=True)

    def save(self, *args, **kwargs) -> None:
        if not self.id:
            self.slug = generateSlug(self.product_name , Products)
        return super().save(*args, **kwargs)



class Skills(models.Model):
    skill_name = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.skill_name

class Person(models.Model):
    person_name = models.CharField(max_length=100)
    skill = models.ManyToManyField(Skills)


class Sudent2(models.Model):
    name = models.CharField(max_length=40)
    age = models.IntegerField()
    gender = models.CharField(max_length=100, null=True , blank = True)
    upload_file = models.FileField(upload_to="files/" ,null=True , blank = True)





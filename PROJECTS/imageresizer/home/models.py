from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from PIL import Image
import os

class Student(models.Model):
    stundent_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10 , choices=(("Male", "Male"), ("Female", "Female")))
    student_id = models.CharField(max_length=10 , null=True , blank=True)


class ImageModel(models.Model):
    original_image = models.ImageField(upload_to="images/")
    thumbnail_mini = models.ImageField(upload_to="images/thumbnails", null=True , blank=True)
    thumbnail_small = models.ImageField(upload_to="images/thumbnails", null=True , blank=True)
    thumbnail_medium = models.ImageField(upload_to="images/thumbnails", null=True , blank=True)
    thumbnail_large = models.ImageField(upload_to="images/thumbnails", null=True , blank=True)




@receiver(post_save, sender =ImageModel)
def create_thumbails(sender , instance , created, **kwargs):
    if created:
        sizes = {
            "thumbnail_mini" : (50 , 50),
            "thumbnail_small" : (100,100),
            "thumbnail_medium" : (300 , 300),
            "thumbnail_large" : (600 ,600) 
        }



        for fields , size in sizes.items():
            img = Image.open(instance.original_image.path)
            img.thumbnail(size, Image.Resampling.LANCZOS)
            thumb_name, thumb_extension = os.path.split(instance.original_image.name)
            thumb_extension = thumb_extension.lower()
            thumb_filename  = f"{thumb_name}_{size[0]}X{size[1]}{thumb_extension}"
            thumb_path = f"thumnails/{thumb_filename}"
            img.save(thumb_path)
            setattr(instance, fields, thumb_path)







@receiver(pre_delete, sender =Student)
def save_student(sender , instance , **kwargs):
    print("OBJ getting deleted")
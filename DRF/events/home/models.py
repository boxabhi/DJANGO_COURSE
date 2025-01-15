from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    def __str__(self):
        return self.category_name

class Event(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True,blank=True)
    event_name = models.CharField(max_length=100)
    event_slug = models.SlugField()
    event_image = models.FileField(upload_to="events/")
    event_price = models.FloatField()

    def __str__(self):
        return self.event_name


    def save(self ,*args, **kwargs):
        if not self.event_slug:
            self.event_slug = slugify(self.event_name)
            if Event.objects.filter(event_slug=self.event_slug).exists():
                self.event_slug = f"{self.event_slug}-{self.id}"
        super().save(*args,**kwargs)


class Booking(models.Model):
    user = models.ForeignKey(User,related_name="bookings", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booking_people_count = models.IntegerField(default=1)

    def __str__(self):
        return self.event.event_name
    
    def total_cost(self):
        return self.event.event_price * self.booking_people_count
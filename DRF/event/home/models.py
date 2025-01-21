from django.db import models
from django.contrib.auth.models import User



class Event(models.Model):
    title = models.CharField(max_length = 255)
    description = models.TextField()
    date = models.DateField()
    capacity = models.IntegerField()
    ticket_price = models.FloatField(default=100)
    status = models.CharField(max_length=255, 
                              default=(('Upcoming', 'Upcoming'), ('Cancelled', 'Cancelled'), ('Happening', 'Happening')))
    image = models.ImageField(upload_to='event_images', blank=True, null=True)



class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=255, choices=(('VIP', 'VIP'), ('Regular', 'Regular')))
    total_person = models.IntegerField(default=1)

class Booking(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=255,default='Pending')
    total_price = models.FloatField()


class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()



class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies'
    )
    post = models.ForeignKey(
        Post, null=True, blank=True, on_delete=models.CASCADE, related_name='comments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:30]
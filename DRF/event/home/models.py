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

data = [
    {
       "first_name" :  "Akash",
        "last_name" :  "Singh",
        "age" : 23
    },{
        "first_name" :  "Rahul",
        "last_name" :  "Singh",
        "age" : 23
    },
    {
        "first_name" :  "Rohit",
        "last_name" :  "Singh",
        "age" : 23
    },{
        "first_name" :  "Raj",
        "last_name" :  "Mishra",
        "age" : 45
    }
]
for d in data:
    Student.objects.create(**d)

search = "Rohit Singh"
student = Student.objects.filter(
    Q(first_name__icontains=search) | Q(last_name__icontains=search))

search = "Rohit Signh"
search = search.split()
["Rohit"]
student = Student.objects.filter(
    Q(first_name__icontains=search[0]) & 
    Q(last_name__icontains=search[1]))

student = Student.objects.filter(
    first_name__icontains=search[0],
    last_name__icontains=search[1])

student = Student.objects.filter(
    Q(first_name__search="Rohit Singh") |
    Q(last_name__search=search))


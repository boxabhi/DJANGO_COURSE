from django.shortcuts import render
import random
from home.rabbitmq import publish_message
from faker import Faker
fake = Faker()



def index(request):
    messsage = f"This is a demo message - {random.randint(0 , 100)}"
    names = [
        {"name": fake.name(), "address": fake.address()} for _ in range(10)
    ]

    publish_message(names)
    return render(request, 'index.html')
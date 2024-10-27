from django.shortcuts import render

# Create your views here.
from .models import Customer

def index(request):
    return render(request, 'admin.html')


def customers(request):
    customers = Customer.objects.all()
    return render(request, 'customers.html', context={'customers' : customers})

def create_customer(request):
    return render(request, 'create_customer.html')
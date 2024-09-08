from django.shortcuts import render, redirect
from .models import *

def home(request):
    pizzas = Pizza.objects.all()
    orders = Order.objects.all()
    return render(request, 'index.html', context = {"pizzas" :pizzas,"orders":orders})

def order(request , order_id):
    try:
        order = Order.objects.get(order_id = order_id)
        return render(request , 'order.html', context = {"order" : order})
    except Exception as e:
        print(e)
        return redirect('/')

def order_pizza(request, pizza_id):
    pizza = Pizza.objects.get(id = pizza_id)
    Order.objects.create(
        pizza = pizza,
        user = request.user,
        amount = pizza.price
    )
    
    return redirect('/')

    
    
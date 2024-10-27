from django.shortcuts import render, redirect
from django.contrib import messages

from django.db.models import Sum
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Customer

# Create your views here.

def registration(request):
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('phone_number')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = Customer.objects.filter(
           username = username)

        if user_obj.exists():
            messages.error(request, 'Error: Username or Email already exists')
            return redirect('/accounts/registration/')
        
        user_obj = Customer.objects.create(
           first_name = first_name,
            last_name = last_name,
            username = username,
            email = email    
        )
        user_obj.set_password(password)
        user_obj.save()
        messages.error(request, 'Success : Account created')
        return redirect('/')

    return render(request , 'registration.html')


def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('phone_number')
        password = request.POST.get('password')
        user_obj = Customer.objects.filter(
          username = username
            )
        if not user_obj.exists():
            messages.debug(request, "1")
            messages.error(request, 'Error: Username does not exist')
            return redirect('/')

       
        user_obj = authenticate(username = username , password = password)

        if not user_obj:
            messages.error(request, 'Error: Invalid credentials')
            return redirect('/')
        
        login(request, user_obj)
        return redirect('/')
        

    return redirect('/')

def logout_page(request):
    logout(request)
    messages.error(request, 'Success:Logged successfull')
    return redirect('/')

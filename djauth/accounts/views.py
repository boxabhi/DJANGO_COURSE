from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .emailer import sendOtpToEmail
import random
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


from django.core.cache import cache

from django.contrib import messages

User = get_user_model()
from .tasks import add


def login_page(request):
    result = (add.delay(4 , 4))
    print(result)
    if request.method == "POST":
        phone_number = request.POST.get('phone_number')
        if cache.get(phone_number):
            data = cache.get(phone_number)
            print(data)
            data['count'] += 1
            if data['count'] >= 3:
                cache.set(phone_number, data, 60 * 5)
                messages.error(request, "You can request OTP after 5 mins.")
                return redirect('/') 
            
            cache.set(phone_number, data, 60 * 1)

        if not cache.get(phone_number):
            data = {
                'phone_number' : phone_number,
                'count' : 1
            }
            cache.set(phone_number, data, 60 * 1)

        user_obj = User.objects.filter(phone_number = phone_number)
        if not user_obj.exists():
            return redirect('/')
        email = user_obj[0].email
        otp = random.randint(1000, 9999)
        user_obj.update(otp = otp)
        subject = "OTP for Login"
        message  = f"You otp is {otp}"

        sendOtpToEmail(
            email,subject, message
        )

        return redirect(f'/check-otp/{user_obj[0].id}/') 

    return render(request, 'login.html')




def check_otp(request, user_id):

            
    if request.method == "POST":
        user_obj = User.objects.get(id = user_id)
        if cache.get(user_obj.phone_number):
            data = cache.get(user_obj.phone_number)
            if data['count'] >= 3:
                messages.error(request, "You can request OTP after 5 mins.")
                return redirect('/') 
            
        otp = request.POST.get('otp')
        print(type(otp), type(user_obj.otp))
        if int(otp) == user_obj.otp:
            login(request, user_obj)
            return redirect('/dashboard/') 
        messages.error(request, "Invald OTP.")
        return redirect(f'/check-otp/{user_obj.id}/') 
    
    return render(request, 'check_otp.html')


@login_required(login_url='/')
def dashboard(request):
    return HttpResponse("You are logged in")
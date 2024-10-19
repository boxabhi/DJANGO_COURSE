from django.shortcuts import render, redirect
from django.contrib import messages
from tracker.models import Transaction
from django.db.models import Sum
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(
            Q(email = email) |  Q(username = username)
            )

        if user_obj.exists():
            messages.error(request, 'Error: Username or Email already exists')
            return redirect('/registration/')
        
        user_obj = User.objects.create(
           first_name = first_name,
            last_name = last_name,
            username = username,
            email = email    
        )
        user_obj.set_password(password)
        user_obj.save()
        messages.error(request, 'Success : Account created')
        return redirect('/registration/')

    return render(request , 'registration.html')


def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(
          username = username
            )
        if not user_obj.exists():
            messages.error(request, 'Error: Username does not exist')
            return redirect('/login/')

       
        user_obj = authenticate(username = username , password = password)

        if not user_obj:
            messages.error(request, 'Error: Invalid credentials')
            return redirect('/login/')
        
        login(request, user_obj)
        return redirect('/')
        

    return render(request , 'login.html')

def logout_page(request):
    logout(request)
    messages.error(request, 'Success:Logged successfull')
    return redirect('/login/')


@login_required(login_url='/login/')
def index(request):

    if request.method == "POST":
        description = request.POST.get('description')
        amount = request.POST.get('amount')

        if description is None:
            messages.info(request, "Description Cannot be blank")
            return redirect('/')
        

        try:
            amount = float(amount)
        except Exception as e:
            messages.info(request, "Should be a Number")
            return redirect('/')
        
        Transaction.objects.create(
            description = description,
            amount = amount,
            created_by = request.user
        )


        return redirect('/')


    context = {
        'transactions' : Transaction.objects.filter(created_by = request.user),
               'balance' : Transaction.objects.filter(created_by = request.user).aggregate(total_balance = Sum('amount'))['total_balance'] or 0,
               'income' : Transaction.objects.filter(created_by = request.user,amount__gte = 0).aggregate(income = Sum('amount'))['income'] or 0,
               'expense' : Transaction.objects.filter(created_by = request.user,amount__lte = 0).aggregate(expense = Sum('amount'))['expense'] or 0,

               }
    
    return render(request, 'index.html', context)


@login_required(login_url='/login/')
def deleteTransaction(request,uuid):
    
    Transaction.objects.get(uuid = uuid).delete()
    return redirect('/')

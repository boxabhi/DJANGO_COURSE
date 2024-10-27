from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Cart,CartItems,Customer
from .models import VendorProducts
from django.contrib import messages

# Create your views here.


@login_required(login_url="/accounts/login/")
def get_cart(request):
    cart = None
    try:
        cart = Cart.objects.get(customer = request.user.customer)
    except Exception as e:
        print(e)
    return render( request,'cart.html', context = {'cart' : cart})


@login_required(login_url="/accounts/login/")
def add_to_cart(request):
    try:
        customer = Customer.objects.get(user_ptr=request.user.id)
        product = request.GET.get('product_id')
        cart , _ = Cart.objects.get_or_create(customer = customer, is_paid=False)
        cart_item , _  = CartItems.objects.get_or_create(cart = cart ,
                                                          product = VendorProducts.objects.get(id = product))
        cart_item.quantity += 1
        cart_item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    except Exception as e:
        messages.error(request, 'Invalid Product ID')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
@login_required(login_url="/accounts/login/")
def remove_to_cart(request):
    try:
        customer = Customer.objects.get(user_ptr=request.user.id)
        product = request.GET.get('product_id')
        quantity = request.GET.get('quantity')

        cart , _ = Cart.objects.get_or_create(customer = customer, is_paid=False)
        cart_item   = CartItems.objects.filter(cart = cart ,product = VendorProducts.objects.get(id = product))

        if cart_item.exists():
            cart_item = cart_item[0]
            if quantity:
                cart_item.quantity = int(quantity)
            else:
                cart_item.quantity -= 1

            if cart_item.quantity <= 0:
                cart_item.delete()
            else:
                cart_item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    except Exception as e:
        print(e)
        messages.error(request, 'Invalid Product ID')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
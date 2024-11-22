from django.urls import path
from .views import *

urlpatterns = [
    path('cart/',get_cart),
    path('add-to-cart/', add_to_cart),
    path('remove-cart-item/', remove_to_cart),
    path('success/', payment_success)
]

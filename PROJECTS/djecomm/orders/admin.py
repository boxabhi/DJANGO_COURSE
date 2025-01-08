from django.contrib import admin
from .models import Cart, CartItems,Order, OrderItems


admin.site.register(Cart)
admin.site.register(CartItems)

admin.site.register(Order)
admin.site.register(OrderItems)
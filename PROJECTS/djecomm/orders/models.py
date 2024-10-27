from django.db import models
from accounts.models import Customer
from products.models import VendorProducts
from django.db.models import Sum,F



class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer_cart")
    is_paid = models.BooleanField(default=False)
   
    def calculateDeliveryFee(self):
        total = self.cart_items.aggregate(
            total = Sum(F('product__delivery_fee'))
        )['total']
        return total or 0

    def getCartTotal(self):
        total = self.cart_items.aggregate(
            total = Sum(F('product__vendor_selling_price') * F('quantity'))
        )['total']
        return total or 0
    







    
    

class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(VendorProducts, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0)

    def getCartItemTotal(self):
        return self.product.vendor_selling_price * self.quantity 
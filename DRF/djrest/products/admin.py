from django.contrib import admin

# Register your models here.


from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'product_brand']

admin.site.register(Product, ProductAdmin)
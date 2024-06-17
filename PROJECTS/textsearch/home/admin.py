from django.contrib import admin
from .models import *
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "description",
        "category",
        "price",
        "brand",
        "sku",
    ]

admin.site.register(Product, ProductAdmin)
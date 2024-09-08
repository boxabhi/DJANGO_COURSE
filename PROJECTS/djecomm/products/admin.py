from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(BrandName)


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "category",
        "sub_category",
        "brand",
        "item_name",
        "product_description",
        "product_sku",
        "hsn_code",
        "parent_product",
        "maximum_retail_price",

        ]
    
    search_fields = [
        "item_name",
        "product_description",
        "product_sku",
        "hsn_code",
    ]



admin.site.register(Products,ProductAdmin)
admin.site.register(VariantOptions)
admin.site.register(ProductVariant)
admin.site.register(ProductImages)
admin.site.register(VendorProducts)
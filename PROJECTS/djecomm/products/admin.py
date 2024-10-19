from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(BrandName)


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "category",
        "item_name",
        "parent_product",
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


class VendorProductsAdmin(admin.ModelAdmin):
    search_fields = ['product__item_name', 'shopkeeper__bmp_id', 'product__product_sku']
    

class ProductVariantAdmin(admin.ModelAdmin):
    search_fields = ['product__item_name',  'product__product_sku']


admin.site.register(Products,ProductAdmin)
admin.site.register(VariantOptions)
admin.site.register(ProductVariant,ProductVariantAdmin)
admin.site.register(ProductImages)
admin.site.register(VendorProducts,VendorProductsAdmin)
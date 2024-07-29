from django.contrib import admin
from home.models import Product
from django.utils.html import format_html



class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "image",
        "description",
        "category",
        "brand",
        "sku",
    )

    def product_id(self , obj):
        return f"PROD_{obj.id}"
    
    def image(self, obj):
        return format_html(
            f"<img src='{obj.thumbnail}' height='30'>"      
        )


    list_filter = ['category']
    search_fields = ('title','description', 'category', 'brand')
    ordering = ('title',)

admin.site.register(Product, ProductAdmin)


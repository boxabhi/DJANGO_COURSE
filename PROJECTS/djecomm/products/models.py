from django.db import models
from utils.models import BaseModel
from accounts.models import Shopkeeper


class Category(BaseModel):
    name = models.CharField(max_length=100)
    comission_percentage = models.IntegerField(default=10)

    def __str__(self) -> str:
        return self.name

class SubCategory(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, 
                                 related_name="sub_categories")
    name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.name

class BrandName(BaseModel):
    name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.name


class Products(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product_category")
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="product_sub_category")
    brand = models.ForeignKey(BrandName, on_delete=models.CASCADE, related_name="product_brand")
    item_name = models.CharField(max_length=1000)
    product_description = models.TextField()
    product_sku = models.CharField(max_length=1000, unique=True)
    hsn_code = models.CharField(max_length=1000, null=True, blank=True)
    parent_product = models.ForeignKey("Products", related_name="variant_products", on_delete=models.CASCADE, null=True , blank=True)
    maximum_retail_price = models.FloatField()

    def __str__(self) -> str:
        return self.product_sku
    
    def getFirstImage(self):
        if self.product_images.first():
            return  self.product_images.first().image

        return "https://static.vecteezy.com/system/resources/thumbnails/022/014/063/small/missing-picture-page-for-website-design-or-mobile-app-design-no-image-available-icon-vector.jpg"
    
    
    def getPdfFirstImage(self):
        if self.product_images.first():
            return f"http://127.0.0.1:8000/media/{self.product_images.first().image}" 

        return "https://static.vecteezy.com/system/resources/thumbnails/022/014/063/small/missing-picture-page-for-website-design-or-mobile-app-design-no-image-available-icon-vector.jpg"
    

class VariantOptions(BaseModel):
    variant_name = models.CharField(max_length=100)
    option_name = models.CharField(max_length=100)

    def __str__(self):
        return self.variant_name + " " + self.option_name


class ProductVariant(BaseModel):
    product = models.ForeignKey(Products, related_name="product_variants", on_delete=models.CASCADE)
    variant_option = models.ManyToManyField(VariantOptions)

class ProductImages(BaseModel):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to="products/images/")


class VendorProducts(BaseModel):
    shopkeeper = models.ForeignKey(Shopkeeper, on_delete=models.CASCADE, related_name="shopkeeper_products")
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="products")
    vendor_selling_price = models.FloatField()
    dealer_price = models.FloatField()
    is_active = models.BooleanField(default=True)
    delivery_fee = models.FloatField(default=0)


    def get_product_details(self):
        return {
            "product_name"  : self.product.item_name,
            "image" : self.getFirstImage()
        } 



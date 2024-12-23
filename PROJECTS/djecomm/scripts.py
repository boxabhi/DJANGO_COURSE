import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'djecomm.settings'
django.setup()
from products.models import *
import pandas as pd
from django.db import transaction
import random

VOLUME_CHOICES = ['500ml', '1L', '2L', '250ml', '100ml']
COLOR_CHOICES = ['Red', 'Blue', 'Green', 'Yellow']
WEIGHT = ['500g', '1kg', '2kg']


def generate_random_option(variant):
    if variant == "Volume":
        return random.choice(VOLUME_CHOICES)
    elif variant == "Colour":
        return random.choice(COLOR_CHOICES)
    elif variant == "Display weight":
        return random.choice(WEIGHT)
    else:
        return f"{variant}-{random.randint(1, 100)}"
    

def upload_products_from_excel(file_path):
    try:
        df = pd.read_excel(file_path)
        with transaction.atomic():
            for index,row in df.iterrows():
                category, _ = Category.objects.get_or_create(name = row['Material category'])
                subcategory,_ = SubCategory.objects.get_or_create(
                    category = category,
                    name = row['Sub category level 1']
                )

                brand, _ = BrandName.objects.get_or_create(name = row['Brand name'])

                if row['Variation type'] in ['Parent only','Parent with variant/s']:
                    parent_product = Products.objects.create(
                        category = category,
                        sub_category = subcategory,
                        brand = brand,
                        item_name = row['Item name title'],
                        product_sku = row['MOB SKU'],
                        product_description = row['Product description'],
                        hsn_code = row['HSN code'],
                        maximum_retail_price = random.randint(1000, 99999))
                
                    if row['Variation type'] == 'Parent with variant/s':
                        variant_theme = row['Variation_theme']
                        variants = variant_theme.split("+")
                        for variant in variants:
                            option_name = generate_random_option(variant)
                            variant_option , _ = VariantOptions.objects.get_or_create(
                                variant_name = variant,
                                option_name = option_name
                            )

                if row['Variation type'] == 'Variant':
                    parent_product = Products.objects.get(product_sku = row['Parent SKU'])
                    variant_options = []
                    parent_variant_options = []

                    variant_theme = row['Variation_theme']
                    variants = variant_theme.split("+")
                    for variant in variants:
                        option_name = generate_random_option(variant)
                        variant_option , _ = VariantOptions.objects.get_or_create(
                            variant_name = variant,
                            option_name = option_name
                        )
                        variant_options.append(variant_option)

                    for variant in variants:
                        option_name = generate_random_option(variant)
                        variant_option , _ = VariantOptions.objects.get_or_create(
                            variant_name = variant,
                            option_name = option_name
                        )
                        parent_variant_options.append(variant_option) 

                    variant_product = Products.objects.create(
                        category = category,
                        sub_category = subcategory,
                        brand = brand,
                        item_name = row['Item name title'],
                        product_sku = row['MOB SKU'],
                        product_description = row['Product description'],
                        hsn_code = row['HSN code'],
                        parent_product = parent_product,
                        maximum_retail_price = random.randint(1000, 99999))
                    
                    parent_product_variant = ProductVariant.objects.create(product = parent_product)
                    parent_product_variant.variant_option.add(*parent_variant_options)
                    product_variant = ProductVariant.objects.create(product = variant_product)
                    product_variant.variant_option.add(*variant_options)

    except Exception as e:
        print(e)

import random

def createVendorProducts():
    vendor = Shopkeeper.objects.first()
    for product in Products.objects.all():
        price = random.randint(100, 10000)
        if VendorProducts.objects.filter(product = product, shopkeeper = vendor):
            continue
        VendorProducts.objects.create(
            shopkeeper = vendor,
            product = product,
            vendor_selling_price = price,
            dealer_price  = price - random.randint(10, 99),
        
        )



from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


def list_files(start_path):
    print(start_path)
    all_files = []
    for root,dirs, files in os.walk(start_path):
        all_files.extend(
            {"path": os.path.join(root, filename), "file": filename}
            for filename in files
        )

    return all_files
def getProductFromImageName(imageName):
    print(imageName)

    try:
        # imageName = imageName.spilt('.')[0]
        print(imageName)
        return True , Products.objects.get(product_sku = imageName), imageName
    except Exception as e:
        print(e)
    
    return False , "", "imageName"


def is_image(file_path):
    try:
        with Image.open(file_path) as img:
            return True
        
    except Exception as e:
        return False
    



def uploadImages(path):
    dir_path = f"{path}"


    file_lists = list_files(dir_path)

    for file_list in file_lists:

        try:
            filename = file_list['file']
            path = file_list['path']
            filename_without_extension = os.path.splitext(filename)[0]
        
            if is_image(path):
                status, sku, image_name = getProductFromImageName(filename_without_extension)
                print(status)
                if status:
                    with open(path, 'rb') as file:
                        upload_file = SimpleUploadedFile(path, file.read())
                        ProductImages.objects.create(
                            product = sku,
                            image = upload_file
                        )
            
        except Exception as e:
            print(e)
            #return False
        

# uploadImages("D:\\DJANGO_COURSE\\firstproject\\PROJECTS\\djecomm\\images")

# createVendorProducts()
# upload_products_from_excel('product.xlsx')

import razorpay
from django.conf import settings
class RazorPayPayment:

    def __init__(self, currency="INR"):
        self.currency = currency
        self.client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))

    def processPayment(self, amount, receipt):
        payment = self.client.order.create({
            "amount": amount,
            "currency": self.currency,
            "receipt": receipt,
            "partial_payment":False,
            "notes": {}
        })
        print(payment)


# payment = RazorPayPayment("INR")
# payment.processPayment(435* 100,"Abhijeet")

from datetime import datetime
from django.template.loader import get_template
from django.conf import settings
import pdfkit
from orders.models import *
from utils.utility import *
order = Order.objects.last()
generateOrderPdf(order, order.getOrderData())


def generateOrderPdf(instance,data):
    dynamic_directory_name = f"public/static/pdfs/{instance.order_id}.pdf"
    template_name = "invoice"

    options = {
    'page-size': 'Letter',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'custom-header': [
        ('Accept-Encoding', 'gzip')
    ],
    
    'no-outline': None
}
    path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    template = get_template(f"{template_name}.html")
    content = template.render(data)
    exact_file_path = f"{settings.BASE_DIR}/{dynamic_directory_name}"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_string(content, exact_file_path, options = options, configuration=config)





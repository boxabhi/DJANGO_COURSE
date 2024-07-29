import os

import django
import itertools
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'textsearch.settings'
django.setup()
import django
import random
from faker import Faker

from datetime import datetime, timedelta
from django.db.models import Avg, Sum, Min, Max, Count, Q
from django.db.models import Subquery, OuterRef
from home.models import Product
import requests


# url = "https://dummyjson.com/products?limit=1000"
# response = requests.get(url)
# data = response.json()


# for product_data in data['products']:
#     try:
#         print(product_data.get('brand'))
#         product = Product(
#             title=product_data['title'],
#             description=product_data['description'],
#             category=product_data['category'],
#             price=product_data['price'],
#             brand=product_data.get('brand'),
#             sku=product_data['sku'],
#             thumbnail=product_data['thumbnail']
#         )
#         product.save()

#     except Exception as e:
#         print(e)

import random
import uuid
url = 'https://fakestoreapi.com/products'
response = requests.get(url)
products = response.json()

for item in products:
    product, created = Product.objects.get_or_create(
        title=item['title'],
        defaults={
            'description': item['description'],
            'category': item['category'],
            'price': item['price'],
            'thumbnail': item['image'],
            'sku' : str(uuid.uuid4()).split('-')[0]
        }
    )
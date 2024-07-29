import os

import django
import itertools
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'elasticproject.settings'
django.setup()
import django
import random
from faker import Faker

from datetime import datetime, timedelta
from django.db.models import Avg, Sum, Min, Max, Count, Q
from django.db.models import Subquery, OuterRef
from products.models import Product, Brand
import requests
from products.documents import ProductDocument


products = Product.objects.all()

for product in products:
    try:
        brand , _ = Brand.objects.get_or_create(brand_name = product.brand)
        product.brand_name = brand
        product.save()
    except Exception as e:
        print(e)



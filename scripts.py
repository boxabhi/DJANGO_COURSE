import os

import django
import itertools
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'firstproject.settings'
django.setup()
import django
import random
from faker import Faker
from home.models import Author, Book
from datetime import datetime, timedelta
from django.db.models import Avg, Sum, Min, Max, Count, Q
from django.db.models import Subquery, OuterRef
from home.models import Products, Brand






product = Products.objects.get(id =11)
product.product_name = "trimmer men with blade 2mm blade"
product.save()

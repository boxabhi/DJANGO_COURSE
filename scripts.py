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


from django.db.models.functions import ExtractMonth

def handle(self, *args, **kwargs):
        # Annotate each book with the month of its published date
        books_each_month = Book.objects.filter(
            author=OuterRef('pk'),
            published_date__year=2023
        ).annotate(month=ExtractMonth('published_date')).values('month').distinct()

        # Aggregate the months into an array
        authors = Author.objects.annotate(
            books_each_month=ArrayAgg(books_each_month.values('month'), distinct=True)
        )

        for author in authors:
            print(f"Author: {author.name}, Months with Books Published in 2023: {author.books_each_month}")
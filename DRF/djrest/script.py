import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'djrest.settings'
django.setup()

from home.models import *
from django.db.models import DecimalField,ExpressionWrapper,IntegerField,Case, When, Value, CharField, F, Q, Count, Sum, Avg, Max, Min


def product_discount():
    products = Product.objects.annotate(
        discount = Case(
            When(price__gte=50, then=Value(10)),
            default=Value(5),
            output_field=IntegerField()
        ),
        disounted_price = ExpressionWrapper(
            F('price') - F('price') * F('discount') / 100,
            output_field=DecimalField()
        )
    )

    for product in products:
        print(product.name, product.price, product.discount, product.disounted_price)


book = Book.objects.first()
print(book.author)

author = Author.objects.first()
print(author.author_books.all())

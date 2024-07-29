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


# Create an instance of Faker
fake = Faker()

# Function to generate fake data for Author
def create_fake_author():
    author_name = fake.name()
    return Author.objects.create(author_name=author_name)

# Function to generate fake data for Book
def create_fake_book(authors):
    book_name = fake.sentence(nb_words=6)
    author = random.choice(authors)
    published_date = fake.date_between(start_date='-2y', end_date='today')
    price = round(random.uniform(10, 100), 2)
    return Book.objects.create(
        book_name=book_name, author=author, published_date=published_date, price=price
    )

# Generate fake data
def generate_fake_data(num_authors, num_books_per_author):
    authors = []
    for _ in range(num_authors):
        author = create_fake_author()
        authors.append(author)

    for _, author in itertools.product(range(num_books_per_author), authors):
        create_fake_book([author])

# Usage

num_authors = 10  # Number of fake authors
num_books_per_author = 5  # Number of fake books per author
generate_fake_data(num_authors, num_books_per_author)
print("Fake data generated successfully!")

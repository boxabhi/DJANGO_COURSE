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
from home.models import *


fake = Faker()

def createPerson(number):
    create = [Person(person_name =fake.name() ) for _ in range(number)]
    Person.objects.bulk_create(create)

def deletePerson(number):

    Person.objects.all().delete()


def updatePerson(name):
    for person in Person.objects.filter(person_name__icontains = name):
        person.person_name = "Abhijeet GUpta"
    print(Person.objects.filter(person_name__icontains = name).count())
    print(Person.objects.filter(person_name__icontains = name).update(person_name="Abhijeet Gupta"))


# deletePerson(1000)

# createPerson(10000)

updatePerson("Davis")




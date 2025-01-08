from .models import *
from faker import Faker
import random
from home.models import Customer, Order
def handle():
    fake = Faker()
    
    # Clear existing data
    Customer.objects.all().delete()
    Order.objects.all().delete()

    # Generate fake customers
    customers = []
    for _ in range(50):  # Generate 50 customers
        customer = Customer(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            phone_number=fake.phone_number(),
            address=fake.address(),
        )
        customer.save()
        customers.append(customer)

 
    # Generate fake orders
    statuses = ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']
    for _ in range(200):  # Generate 200 orders
        order = Order(
            customer=random.choice(customers),
            order_date=fake.date_this_year(),
            total_amount=round(random.uniform(50.0, 500.0), 2),
            status=random.choice(statuses)
        )
        order.save()

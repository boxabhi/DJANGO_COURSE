from locust import HttpUser, task , between
from faker import Faker
import random
fake = Faker()

class WebsiteUser(HttpUser):

    @task(5)
    def get_products(self):
        self.client.get('/api/products/')

    @task(3)
    def submit_feedback(self):
        payload = {
            "name" : fake.name(),
            "email" : fake.email(),
            "message" : fake.text()
        }
        self.client.post('/api/submit-feedback/', json=payload)

    @task(2)
    def get_details(self):
        product_id = random.randint(1, 500)
        self.client.get(f'/api/products/{product_id}/')
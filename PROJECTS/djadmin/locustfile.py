from locustfile import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):

    @task(1)
    def view_home_page(self):
        # Simulate a user visiting the home page
        response = self.client.get("/")
        # Check if a specific part of the HTML page is present
        if "Welcome" not in response.text:
            print("Home page did not load correctly")

    @task(2)
    def view_customer_page(self):
        # Simulate a user visiting the customer list page
        response = self.client.get("/customers/")
        if "Customer List" not in response.text:
            print("Customer page did not load correctly")

    @task(3)
    def create_order(self):
        # Simulate submitting a form to create an order
        payload = {
            "customer": 1,
            "order_date": "2023-12-01",
            "total_amount": 500.0,
            "status": "Pending"
        }
        # Simulate POST request to create order
        response = self.client.post("/orders/create/", data=payload)
        if response.status_code != 200:
            print("Failed to create order")
        
    @task(4)
    def view_order_detail(self):
        # Simulate visiting an order detail page (e.g., order with ID 1)
        response = self.client.get("/orders/1/")
        if "Order Detail" not in response.text:
            print("Order detail page did not load correctly")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)

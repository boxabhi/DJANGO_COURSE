import razorpay
from django.conf import settings



class RazorPayPayment:

    def __init__(self, currency="INR"):
        self.currency = currency
        self.client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))

    def processPayment(self, amount, receipt):
        payment = self.client.order.create({
            "amount": amount,
            "currency": self.currency,
            "receipt": receipt,
            "partial_payment":False,
            "payment_capture" : "1",
            "notes": {}
        })


        return payment


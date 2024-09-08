
from django.urls import path, include
from .views import *


urlpatterns = [
    path('' ,home, name='home' ),
    path('<order_id>/' , order , name='order'),
    path('order_pizza/<pizza_id>/',order_pizza , name="order_pizza")
]

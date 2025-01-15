from django.urls import path, include
from home.views import (CategoryViewSet, EventViewSet,BookingViewSet)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'events', EventViewSet, basename='event')
router.register(r'bookings', BookingViewSet, basename='bookings')





urlpatterns = [
    path('', include(router.urls))
]



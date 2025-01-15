
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('private/event', views.PrivateEventViewSet, basename='private-event')
router.register('public/event', views.PublicEventViewSet
, basename='public-event')

router.register('booking', views.BookViewSet, basename='booking')


urlpatterns = [
    path('register/', views.ResgiserAPI.as_view()),
    path('login/', views.LoginAPI.as_view()),
    path('', include(router.urls)),

]
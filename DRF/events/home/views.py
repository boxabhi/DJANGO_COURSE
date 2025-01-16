from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer






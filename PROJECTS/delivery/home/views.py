from django.shortcuts import render
from home.models import *
from django.http import JsonResponse


def index(request):
    return render(request, 'index.html')

def get_data(request):
    lastest_data = LocationUpdate.objects.latest('timestamp')
    return JsonResponse({
        "latitude" : lastest_data.latitude,
        "longitude" : lastest_data.longitude,
        "timestamp" : lastest_data.timestamp
    })
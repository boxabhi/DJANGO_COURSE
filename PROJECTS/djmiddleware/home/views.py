from django.shortcuts import render
from django.http import JsonResponse
from .models import Store

# Create your views here.


def index(request):

    print(request.headers)
    store = Store.objects.get(bmp_id = (request.headers.get('bmp')))

    data = {
          "status" : True,
          "message" : "store data",
          "data" : {
              "bmp_id" : store.bmp_id,
             "store_name" : store.store_name
          }
    }
    return JsonResponse(data)


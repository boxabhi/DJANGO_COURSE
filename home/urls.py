
from django.urls import path
from home.views import index , contact,dynamic_route,about,thank_you,search_page


urlpatterns = [
    path('', index),
    path('contact/', contact),
    path('about/', about),
    path('search_page/', search_page),
    path('thank-you/', thank_you,),
    path('dynamic_route/<number>/' , dynamic_route)
   
]

"""
URL configuration for djrest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home.views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'product/v2', ProductViewSet, basename='products')

urlpatterns = [
    path('api/', index , ),
    path('api/student/', student),
    path('api/create_record/', create_record, ),
    path('api/update_record/',update_record),
    path('api/get_records/', get_records ,),
    path('api/delete_record/',delete_record),
    path('api/create_book/', create_book, ),
    path('api/get_book/', get_book, ),
    path('api/create_user/', create_user),
    path('api/v2/student/', StudentAPI.as_view()),
    path('api/v3/student/', StudentModelListView.as_view()),

    path('api/product/',ProductListCreate.as_view()),

    
    path('admin/', admin.site.urls),
]


urlpatterns += router.urls
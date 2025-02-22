
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from debug_toolbar.toolbar import debug_toolbar_urls


router = DefaultRouter()
router.register('private/event', views.PrivateEventViewSet, basename='private-event')
router.register('public/event', views.PublicEventViewSet
, basename='public-event')

router.register('booking', views.BookViewSet, basename='booking')


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('register/', views.ResgiserAPI.as_view()),
    path('login/', views.LoginAPI.as_view()),
    path('', include(router.urls)),

]+ debug_toolbar_urls()
from django.urls import path

from . import views

urlpatterns = [
    path('rooms/mine/', views.my_room, name='api_rooms_mine'),
]
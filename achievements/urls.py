from django.urls import path

from . import views

app_name = 'achievements'

urlpatterns = [
    path('', views.achievement_catalogue, name='achievement_catalogue'),
    path('<int:pk>/', views.achievement_public_detail, name='achievement_detail'),
]
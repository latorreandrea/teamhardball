from django.urls import path

from . import views

app_name = 'achievements'

urlpatterns = [
    path('', views.achievement_catalogue, name='achievement_catalogue'),
    path('<int:pk>/', views.achievement_public_detail, name='achievement_detail'),
    path('<int:pk>/assign/', views.achievement_assign, name='achievement_assign'),
    path('<int:pk>/delete/', views.achievement_delete, name='achievement_delete'),
]
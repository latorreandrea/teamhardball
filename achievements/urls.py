from django.urls import path
from . import views

app_name = 'achievements'

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('mine/', views.achievement_catalogue, name='achievement_catalogue'),
    path('mine/<int:pk>/', views.achievement_public_detail, name='achievement_detail'),
    path('definitions/', views.achievement_definition_list, name='definition_list'),
    path('definitions/new/', views.achievement_definition_create, name='definition_create'),
    path('definitions/<int:pk>/edit/', views.achievement_definition_edit, name='definition_edit'),
    path('definitions/<int:pk>/delete/', views.achievement_definition_delete, name='definition_delete'),
    path('definitions/<int:pk>/', views.achievement_definition_detail, name='definition_detail'),
    path('awards/', views.user_achievement_list, name='award_list'),
    path('awards/new/', views.user_achievement_create, name='award_create'),
]
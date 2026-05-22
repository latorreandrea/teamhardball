from django.urls import path

from . import views

app_name = 'armoury'

urlpatterns = [
    path('', views.equipment_list, name='equipment_list'),
    path('registrer/', views.equipment_create, name='equipment_create'),
    path('<int:pk>/', views.equipment_detail, name='equipment_detail'),
    path('<int:pk>/rediger/', views.equipment_edit, name='equipment_edit'),
    path('<int:pk>/lan/', views.equipment_borrow, name='equipment_borrow'),
    path('<int:pk>/returner/', views.equipment_return, name='equipment_return'),
]

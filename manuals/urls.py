from django.urls import path

from . import views

app_name = 'manuals'

urlpatterns = [
    # Public (login_required)
    path('', views.manual_list, name='manual_list'),
    path('<int:pk>/', views.manual_detail, name='manual_detail'),

    # Staff-only
    path('admin/', views.admin_manual_list, name='admin_manual_list'),
    path('admin/create/', views.admin_manual_create, name='admin_manual_create'),
    path('admin/<int:pk>/edit/', views.admin_manual_edit, name='admin_manual_edit'),
    path('admin/<int:pk>/delete/', views.admin_manual_delete, name='admin_manual_delete'),
]

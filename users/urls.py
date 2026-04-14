from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.profile_area, name='profile_area'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('join/', views.join_request, name='join_request'),
    path('enheden/', views.enheden, name='enheden'),
    
    # Admin dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/kommandostruktur/', views.admin_kommandostruktur, name='admin_kommandostruktur'),
    path('admin-dashboard/kommandostruktur/update-rank/<int:user_id>/', views.update_rank, name='update_rank'),
    path('admin-dashboard/new-recruits/', views.new_recruits, name='new_recruits'),
    path('admin-dashboard/approve/<int:request_id>/', views.approve_request, name='approve_request'),
    path('admin-dashboard/reject/<int:request_id>/', views.reject_request, name='reject_request'),
]

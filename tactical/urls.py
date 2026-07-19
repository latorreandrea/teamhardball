from django.urls import include, path

from . import views

app_name = 'tactical'

urlpatterns = [
    # Staff control-plane (single room — at most one exists at any time)
    path('', views.room_home, name='room_home'),
    path('<int:room_id>/', views.room_edit, name='room_edit'),
    path('<int:room_id>/delete/', views.room_delete, name='room_delete'),
    path('<int:room_id>/toggle/', views.room_toggle_active, name='room_toggle_active'),

    # AJAX — available users for platoon assignment
    path('<int:room_id>/available-users/', views.get_available_users, name='available_users'),

    # Mobile API
    path('api/', include('tactical.api.urls')),
]
from django.urls import path

from . import views

app_name = 'finances'

urlpatterns = [
    # Transaction management (admin/staff + finance view permission)
    path('', views.transaction_list, name='transaction_list'),
    path('create/', views.transaction_create, name='transaction_create'),

    # Expense request management (admin/staff only)
    path('requests/', views.admin_request_list, name='admin_request_list'),
    path('requests/<int:pk>/', views.admin_request_action, name='admin_request_action'),

    # Finance view permissions (admin/staff only)
    path('permissions/', views.permission_list, name='permission_list'),
    path('permissions/grant/', views.permission_grant, name='permission_grant'),
    path('permissions/<int:pk>/revoke/', views.permission_revoke, name='permission_revoke'),

    # Member expense request views
    path('request/', views.expense_request_create, name='expense_request_create'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('request/<int:pk>/clarify/', views.request_clarify, name='request_clarify'),
]
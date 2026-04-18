from django.urls import path

from . import views

app_name = 'comms'

urlpatterns = [
    # Public
    path('', views.PostListView.as_view(), name='post_list'),
    path('news/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('events/<int:event_pk>/rsvp/', views.rsvp, name='rsvp'),

    # Staff-only admin
    path('admin/news/', views.admin_news_list, name='admin_news_list'),
    path('admin/news/create/', views.admin_news_create, name='admin_news_create'),
    path('admin/news/<slug:slug>/edit/', views.admin_news_edit, name='admin_news_edit'),
    path('admin/news/<slug:slug>/delete/', views.admin_news_delete, name='admin_news_delete'),

    path('admin/events/', views.admin_events_list, name='admin_events_list'),
    path('admin/events/create/', views.admin_event_create, name='admin_event_create'),
    path('admin/events/<int:event_pk>/edit/', views.admin_event_edit, name='admin_event_edit'),
    path('admin/events/<int:event_pk>/delete/', views.admin_event_delete, name='admin_event_delete'),
    path('admin/events/<int:event_pk>/attendees/', views.admin_event_attendees, name='admin_event_attendees'),
]

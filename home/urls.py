from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('kontakt/', views.contact, name='contact'),
    path('privatlivspolitik/', views.privacy_policy, name='privacy_policy'),
    path('discord/', views.discord_redirect, name='discord_redirect'),
    path('hq/', views.hq, name='hq'),
]

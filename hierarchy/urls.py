from django.urls import path

from . import views

app_name = "hierarchy"

urlpatterns = [
    path("", views.hierarchy_map, name="hierarchy_map"),
    path("node/opret/", views.node_create, name="node_create"),
    path("node/<int:pk>/rediger/", views.node_edit, name="node_edit"),
    path("node/<int:pk>/slet/", views.node_delete, name="node_delete"),
]

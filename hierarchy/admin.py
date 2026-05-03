from django.contrib import admin

from .models import Node


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ["name", "node_type", "parent", "leader", "order"]
    list_filter = ["node_type"]
    search_fields = ["name"]
    raw_id_fields = ["leader"]
    filter_horizontal = ["members"]
    ordering = ["order", "name"]

from django.contrib import admin

from .models import Equipment


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display  = ['name', 'category', 'owner', 'borrowed_by', 'created_at']
    list_filter   = ['category']
    search_fields = ['name', 'owner__last_name', 'owner__email']
    raw_id_fields = ['owner', 'borrowed_by']

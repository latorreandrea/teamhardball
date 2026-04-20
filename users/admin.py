from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import User, JoinRequest, RankIcon


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for custom User model"""
    
    list_display = ['email', 'first_name', 'last_name', 'rank', 'is_active', 'is_staff']
    list_filter = ['is_staff', 'is_active', 'rank', 'nationality']
    search_fields = ['email', 'first_name', 'last_name', 'nickname']
    ordering = ['last_name', 'first_name']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Information'), {
            'fields': ('first_name', 'last_name', 'nickname', 'nationality', 'residence', 'info')
        }),
        (_('Rank'), {
            'fields': ('rank',)
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important Dates'), {
            'fields': ('last_login', 'date_joined'),
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ['last_login', 'date_joined']


@admin.register(JoinRequest)
class JoinRequestAdmin(admin.ModelAdmin):
    """Admin configuration for Join Request model"""
    
    list_display = ['first_name', 'last_name', 'email', 'phone', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['created_at', 'processed_at', 'processed_by', 'generated_password']
    
    fieldsets = (
        (_('Request Information'), {
            'fields': ('nome', 'cognome', 'email', 'telefono')
        }),
        (_('Status'), {
            'fields': ('status', 'rejection_reason')
        }),
        (_('Processing Information'), {
            'fields': ('created_at', 'processed_at', 'processed_by', 'generated_password')
        }),
    )


@admin.register(RankIcon)
class RankIconAdmin(admin.ModelAdmin):
    """Admin for rank insignia icons. One image per rank; old file is deleted on replace."""

    list_display = ['rank', 'get_rank_display_label', 'icon_preview']
    ordering = ['rank']

    def get_rank_display_label(self, obj):
        return obj.get_rank_display()
    get_rank_display_label.short_description = 'Rang'

    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" style="height:34px;width:auto;border-radius:2px;">',
                obj.icon.url,
            )
        return '–'
    icon_preview.short_description = 'Preview'

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, JoinRequest


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for custom User model"""
    
    list_display = ['email', 'nome', 'cognome', 'rango', 'is_active', 'is_staff']
    list_filter = ['is_staff', 'is_active', 'rango', 'nazionalita']
    search_fields = ['email', 'nome', 'cognome', 'nickname']
    ordering = ['cognome', 'nome']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Informazioni Personali'), {
            'fields': ('nome', 'cognome', 'nickname', 'nazionalita', 'luogo_residenza', 'info')
        }),
        (_('Rango'), {
            'fields': ('rango',)
        }),
        (_('Permessi'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Date Importanti'), {
            'fields': ('last_login', 'date_joined'),
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome', 'cognome', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ['last_login', 'date_joined']


@admin.register(JoinRequest)
class JoinRequestAdmin(admin.ModelAdmin):
    """Admin configuration for Join Request model"""
    
    list_display = ['nome', 'cognome', 'email', 'telefono', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['nome', 'cognome', 'email', 'telefono']
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

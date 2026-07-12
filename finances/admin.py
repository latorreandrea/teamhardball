from django.contrib import admin

from .models import ExpenseRequest, FinanceViewPermission, Transaction


@admin.register(ExpenseRequest)
class ExpenseRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'status', 'created_at', 'processed_at', 'processed_by']
    list_filter = ['status']
    search_fields = ['user__email', 'user__last_name', 'description']
    raw_id_fields = ['user', 'processed_by']
    readonly_fields = ['created_at', 'processed_at']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['entry_type', 'amount', 'description', 'recorded_by', 'incurred_by', 'created_at']
    list_filter = ['entry_type']
    search_fields = ['description', 'incurred_by__last_name', 'note']
    raw_id_fields = ['recorded_by', 'incurred_by', 'expense_request']


@admin.register(FinanceViewPermission)
class FinanceViewPermissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'granted_by', 'created_at']
    raw_id_fields = ['user', 'granted_by']
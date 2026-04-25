from django.contrib import admin
from django.utils.html import format_html

from .models import AchievementDefinition, UserAchievement


@admin.register(AchievementDefinition)
class AchievementDefinitionAdmin(admin.ModelAdmin):
    list_display = ["title", "is_active", "icon_preview", "updated_at"]
    list_filter = ["is_active"]
    search_fields = ["title", "slug", "info"]
    prepopulated_fields = {"slug": ("title",)}

    fieldsets = (
        ("Base", {"fields": ("title", "slug", "info", "icon", "is_active")} ),
    )

    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" style="height:32px;width:32px;object-fit:cover;border-radius:50%;">',
                obj.icon.url,
            )
        return "-"

    icon_preview.short_description = "Icon"


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ["user", "achievement", "source", "awarded_by", "awarded_at"]
    list_filter = ["source", "achievement", "awarded_at"]
    search_fields = [
        "user__email",
        "user__first_name",
        "user__last_name",
        "achievement__title",
        "reason",
    ]
    autocomplete_fields = ["user", "achievement", "awarded_by"]
    readonly_fields = ["awarded_at"]

    def save_model(self, request, obj, form, change):
        if obj.source == UserAchievement.Source.MANUAL and not obj.awarded_by:
            obj.awarded_by = request.user
        if obj.source == UserAchievement.Source.AUTO:
            obj.awarded_by = None
        super().save_model(request, obj, form, change)

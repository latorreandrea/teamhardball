from django.contrib import admin

from .models import Chapter, Manual


class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1
    fields = ['order', 'title', 'content', 'image']
    ordering = ['order']


@admin.register(Manual)
class ManualAdmin(admin.ModelAdmin):
    list_display  = ['title', 'allowed_ranks', 'created_at']
    search_fields = ['title']
    inlines       = [ChapterInline]


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display  = ['manual', 'order', 'title']
    list_filter   = ['manual']
    ordering      = ['manual', 'order']

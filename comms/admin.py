from django.contrib import admin

from .models import Attendance, Event, Post


class EventInline(admin.StackedInline):
    model = Event
    extra = 0


class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [EventInline]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('related_post', 'event_date', 'location', 'max_participants')
    list_filter = ('event_date',)
    search_fields = ('related_post__title', 'location')
    inlines = [AttendanceInline]


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'status')
    list_filter = ('status',)

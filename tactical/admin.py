from django.contrib import admin

from .models import HQPoint, Platoon, Room, RoomAssignment


class PlatoonInline(admin.TabularInline):
    model = Platoon
    extra = 0
    fields = ('name', 'team_leader')


class RoomAssignmentInline(admin.TabularInline):
    model = RoomAssignment
    extra = 0
    fields = ('user', 'platoon', 'role')


class HQPointInline(admin.TabularInline):
    model = HQPoint
    extra = 0
    fields = ('name', 'latitude', 'longitude')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    inlines = [PlatoonInline, RoomAssignmentInline, HQPointInline]


@admin.register(Platoon)
class PlatoonAdmin(admin.ModelAdmin):
    list_display = ('name', 'room', 'team_leader')
    list_filter = ('room',)
    search_fields = ('name',)


@admin.register(RoomAssignment)
class RoomAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'platoon', 'role')
    list_filter = ('room', 'role', 'platoon')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')


@admin.register(HQPoint)
class HQPointAdmin(admin.ModelAdmin):
    list_display = ('name', 'room', 'latitude', 'longitude')
    list_filter = ('room',)
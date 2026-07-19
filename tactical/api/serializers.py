from rest_framework import serializers

from ..models import HQPoint, Room, RoomAssignment, SpawnPoint


class SpawnPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpawnPoint
        fields = ['name', 'latitude', 'longitude']


class HQPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = HQPoint
        fields = ['name', 'latitude', 'longitude']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'bounds_north', 'bounds_south',
                  'bounds_east', 'bounds_west']


class MyRoomSerializer(serializers.Serializer):
    """Response for GET /api/rooms/mine/ — the mobile app bootstrap."""
    room = serializers.SerializerMethodField()
    player = serializers.SerializerMethodField()
    spawn_points = serializers.SerializerMethodField()
    hq_points = serializers.SerializerMethodField()
    websocket_url = serializers.SerializerMethodField()

    def __init__(self, assignment: RoomAssignment, *args, **kwargs):
        self.assignment = assignment
        super().__init__(*args, **kwargs)

    def get_room(self, obj):
        room = self.assignment.room
        return {
            'id': room.id,
            'name': room.name,
            'bounds': {
                'north': room.bounds_north,
                'south': room.bounds_south,
                'east': room.bounds_east,
                'west': room.bounds_west,
            },
        }

    def get_player(self, obj):
        return {
            'id': self.assignment.user.id,
            'name': self.assignment.user.get_full_name(),
            'platoon': (
                self.assignment.platoon.name
                if self.assignment.platoon else None
            ),
            'role': self.assignment.role,
        }

    def get_spawn_points(self, obj):
        return [
            {'name': sp.name, 'lat': sp.latitude, 'lng': sp.longitude}
            for sp in self.assignment.room.spawn_points.all()
        ]

    def get_hq_points(self, obj):
        return [
            {'name': hp.name, 'lat': hp.latitude, 'lng': hp.longitude}
            for hp in self.assignment.room.hq_points.all()
        ]

    def get_websocket_url(self, obj):
        return f'/ws/room/{self.assignment.room.id}/'
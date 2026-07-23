from rest_framework import serializers

from ..models import HQPoint, Room, RoomAssignment


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
    members = serializers.SerializerMethodField()
    hq_points = serializers.SerializerMethodField()
    websocket_url = serializers.SerializerMethodField()

    def __init__(self, assignment: RoomAssignment, *args, **kwargs):
        self.assignment = assignment
        super().__init__(instance=assignment, *args, **kwargs)

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
            'platoon_id': (
                self.assignment.platoon_id
            ),
            'platoon': (
                self.assignment.platoon.name
                if self.assignment.platoon else None
            ),
            'role': self.assignment.role,
        }

    def get_members(self, obj):
        assignments = (
            RoomAssignment.objects
            .select_related('user', 'platoon')
            .filter(room=self.assignment.room)
        )
        return [
            {
                'id': ra.user.id,
                'name': ra.user.get_full_name(),
                'platoon': ra.platoon.name if ra.platoon else None,
                'role': ra.role,
            }
            for ra in assignments
        ]

    def get_hq_points(self, obj):
        return [
            {'name': hp.name, 'lat': hp.latitude, 'lng': hp.longitude}
            for hp in self.assignment.room.hq_points.all()
        ]

    def get_websocket_url(self, obj):
        return f'/ws/room/{self.assignment.room.id}/'

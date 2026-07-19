import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class RoomConsumer(AsyncJsonWebsocketConsumer):
    """
    WebSocket consumer for a single tactical room.

    Handles:
      - gps_update: broadcast player position to all in the same room
      - spot_enemy: broadcast enemy spotting to all in the room
      - place_marker: Team Leader places a tactical marker
      - remove_marker: Team Leader removes a tactical marker
    """

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'tactical_room_{self.room_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive_json(self, content, **kwargs):
        """Route incoming messages by type."""
        msg_type = content.get('type')

        if msg_type == 'gps_update':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'broadcast_gps',
                    'user_id': self.scope['user'].id,
                    'user_name': self.scope['user'].get_full_name(),
                    'lat': content['lat'],
                    'lng': content['lng'],
                    'heading': content.get('heading', 0),
                    'speed': content.get('speed', 0),
                    'accuracy': content.get('accuracy', 0),
                },
            )

        elif msg_type == 'spot_enemy':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'broadcast_spot',
                    'spot_id': content.get('spot_id', ''),
                    'lat': content['lat'],
                    'lng': content['lng'],
                    'description': content.get('description', ''),
                    'spotted_by': self.scope['user'].id,
                    'spotted_by_name': self.scope['user'].get_full_name(),
                },
            )

        elif msg_type == 'place_marker':
            # Only Team Leaders can place markers (check done server-side)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'broadcast_marker_placed',
                    'marker_id': content.get('marker_id', ''),
                    'lat': content['lat'],
                    'lng': content['lng'],
                    'marker_type': content['marker_type'],
                    'placed_by': self.scope['user'].id,
                    'placed_by_name': self.scope['user'].get_full_name(),
                },
            )

        elif msg_type == 'remove_marker':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'broadcast_marker_removed',
                    'marker_id': content['marker_id'],
                },
            )

    # === Group event handlers ===

    async def broadcast_gps(self, event):
        """Send GPS update to all clients in the room."""
        await self.send_json({
            'type': 'players_update',
            'players': [{
                'user_id': event['user_id'],
                'name': event['user_name'],
                'lat': event['lat'],
                'lng': event['lng'],
                'heading': event['heading'],
                'speed': event['speed'],
                'accuracy': event['accuracy'],
            }],
        })

    async def broadcast_spot(self, event):
        """Send enemy spotting to all clients in the room."""
        await self.send_json({
            'type': 'enemy_spotted',
            'spot_id': event['spot_id'],
            'lat': event['lat'],
            'lng': event['lng'],
            'description': event.get('description', ''),
            'spotted_by': event['spotted_by'],
            'spotted_by_name': event.get('spotted_by_name', ''),
        })

    async def broadcast_marker_placed(self, event):
        """Send tactical marker placement to all clients in the room."""
        await self.send_json({
            'type': 'marker_placed',
            'marker_id': event['marker_id'],
            'lat': event['lat'],
            'lng': event['lng'],
            'marker_type': event['marker_type'],
            'placed_by': event['placed_by'],
            'placed_by_name': event.get('placed_by_name', ''),
        })

    async def broadcast_marker_removed(self, event):
        """Send tactical marker removal to all clients in the room."""
        await self.send_json({
            'type': 'marker_removed',
            'marker_id': event['marker_id'],
        })
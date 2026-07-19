from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import RoomAssignment
from .serializers import MyRoomSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_room(request):
    """
    Return the room assigned to the currently authenticated user.

    This is the bootstrap endpoint the mobile app calls after login.
    Returns room info, player role/platoon, spawn/HQ points, and WebSocket URL.
    """
    try:
        assignment = (
            RoomAssignment.objects
            .select_related('room', 'platoon')
            .get(user=request.user, room__is_active=True)
        )
    except RoomAssignment.DoesNotExist:
        return Response(
            {'detail': 'No active room assigned.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = MyRoomSerializer(assignment)
    return Response(serializer.data)
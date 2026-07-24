import json
import logging

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import HQPoint, Platoon, Room, RoomAssignment

User = get_user_model()
logger = logging.getLogger(__name__)


@staff_member_required
def room_home(request):
    """
    Single-room entry point: redirect to edit if a room exists, otherwise render
    the creation form. There is always at most one tactical room.
    """
    room = Room.objects.first()

    if room and request.method == 'GET':
        return redirect('tactical:room_edit', room_id=room.id)

    if request.method == 'POST':
        return _handle_room_save(request, room=room)

    users = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
    return render(request, 'tactical/room_form.html', {
        'users': users,
        'is_edit': False,
    })


@staff_member_required
def room_edit(request, room_id):
    """Edit the tactical room."""
    room = get_object_or_404(
        Room.objects.prefetch_related(
            'platoons__members',
            'platoons__team_leader',
            'assignments__user',
            'hq_points',
        ),
        pk=room_id,
    )

    if request.method == 'POST':
        return _handle_room_save(request, room=room)

    users = User.objects.filter(is_active=True).order_by('first_name', 'last_name')

    room_data = {
        'id': room.id,
        'name': room.name,
        'is_active': room.is_active,
        'bounds_north': room.bounds_north,
        'bounds_south': room.bounds_south,
        'bounds_east': room.bounds_east,
        'bounds_west': room.bounds_west,
        'hq_points': [
            {'id': hp.id, 'name': hp.name, 'lat': hp.latitude, 'lng': hp.longitude}
            for hp in room.hq_points.all()
        ],
        'platoons': [
            {
                'id': p.id,
                'name': p.name,
                'team_leader': {
                    'id': p.team_leader.id,
                    'name': p.team_leader.get_full_name(),
                } if p.team_leader else None,
                'members': [
                    {
                        'id': m.user.id,
                        'name': m.user.get_full_name(),
                        'role': m.role,
                    }
                    for m in p.members.select_related('user').all()
                ],
            }
            for p in room.platoons.all()
        ],
    }

    return render(request, 'tactical/room_form.html', {
        'users': users,
        'room': room,
        'room_data_json': json.dumps(room_data),
        'is_edit': True,
    })


@staff_member_required
@require_http_methods(['POST'])
def room_delete(request, room_id):
    """Delete a tactical room."""
    room = get_object_or_404(Room, pk=room_id)
    room.delete()
    return redirect('tactical:room_home')


@staff_member_required
@require_http_methods(['POST'])
def room_toggle_active(request, room_id):
    """Toggle the active status of a room."""
    room = get_object_or_404(Room, pk=room_id)
    room.is_active = not room.is_active
    room.save()
    return redirect('tactical:room_edit', room_id=room.id)


@staff_member_required
def get_available_users(request, room_id):
    """API: return users not yet assigned to any platoon in the given room."""
    room = get_object_or_404(Room, pk=room_id)
    assigned_ids = RoomAssignment.objects.filter(room=room).values_list('user_id', flat=True)
    available = (
        User.objects
        .filter(is_active=True)
        .exclude(id__in=assigned_ids)
        .order_by('first_name', 'last_name')
    )
    return JsonResponse({
        'users': [
            {'id': u.id, 'name': u.get_full_name(), 'rank': u.get_rank_display()}
            for u in available
        ]
    })


def _handle_room_save(request, room=None):
    """Shared logic for creating and updating a room."""
    is_new = room is None

    name = request.POST.get('name', '').strip()
    is_active = request.POST.get('is_active') == 'on'

    if not name:
        return render(request, 'tactical/room_form.html', {
            'error': 'Room name is required.',
            'users': User.objects.filter(is_active=True),
            'room': room,
            'is_edit': not is_new,
        })

    if is_new:
        room = Room(name=name)
    else:
        room.name = name

    room.is_active = is_active
    room.bounds_north = float(request.POST.get('bounds_north', 0))
    room.bounds_south = float(request.POST.get('bounds_south', 0))
    room.bounds_east = float(request.POST.get('bounds_east', 0))
    room.bounds_west = float(request.POST.get('bounds_west', 0))
    room.save()

    # --- HQ Points ---
    existing_hq_ids = set(HQPoint.objects.filter(room=room).values_list('id', flat=True))
    incoming_hq_ids = set()

    hq_names = request.POST.getlist('hq_name[]')
    hq_lats = request.POST.getlist('hq_lat[]')
    hq_lngs = request.POST.getlist('hq_lng[]')
    hq_ids = request.POST.getlist('hq_id[]')

    for i in range(len(hq_names)):
        if not hq_names[i].strip():
            continue
        hq_id = hq_ids[i] if i < len(hq_ids) else ''
        if hq_id and int(hq_id) in existing_hq_ids:
            hp = HQPoint.objects.get(pk=int(hq_id))
            hp.name = hq_names[i]
            hp.latitude = float(hq_lats[i])
            hp.longitude = float(hq_lngs[i])
            hp.save()
            incoming_hq_ids.add(int(hq_id))
        else:
            HQPoint.objects.create(
                room=room,
                name=hq_names[i],
                latitude=float(hq_lats[i]),
                longitude=float(hq_lngs[i]),
            )

    HQPoint.objects.filter(room=room).exclude(id__in=incoming_hq_ids).delete()

    # --- Platoons & Assignments ---
    existing_platoon_ids = set(Platoon.objects.filter(room=room).values_list('id', flat=True))
    incoming_platoon_ids = set()

    platoon_ids = request.POST.getlist('platoon_id[]')
    platoon_names = request.POST.getlist('platoon_name[]')
    platoon_leaders = request.POST.getlist('platoon_leader[]')

    for i in range(len(platoon_names)):
        if not platoon_names[i].strip():
            continue
        p_id = platoon_ids[i] if i < len(platoon_ids) else ''
        if p_id and int(p_id) in existing_platoon_ids:
            platoon = Platoon.objects.get(pk=int(p_id))
        else:
            platoon = Platoon(room=room)
        platoon.name = platoon_names[i]

        leader_id = platoon_leaders[i] if i < len(platoon_leaders) else ''
        platoon.team_leader = User.objects.get(pk=int(leader_id)) if leader_id else None
        platoon.save()
        incoming_platoon_ids.add(platoon.id)

        # Members for this platoon
        member_ids_str = request.POST.get(f'platoon_members_{i}', '')
        member_ids = [int(x) for x in member_ids_str.split(',') if x.strip()]

        # Ensure team leader is always included as a member (RoomAssignment)
        tl_id = platoon.team_leader_id
        if tl_id and tl_id not in member_ids:
            member_ids.append(tl_id)

        # Remove old assignments for this platoon that aren't in the new member list
        RoomAssignment.objects.filter(platoon=platoon).exclude(user_id__in=member_ids).delete()

        for uid in member_ids:
            assignment, created = RoomAssignment.objects.update_or_create(
                room=room,
                user_id=uid,
                defaults={'platoon': platoon},
            )
            # If this member is also the team leader, update their role
            if assignment.user_id == platoon.team_leader_id:
                assignment.role = 'team_leader'
            else:
                assignment.role = 'member'
            assignment.save()

    # Delete platoons that were removed
    Platoon.objects.filter(room=room).exclude(id__in=incoming_platoon_ids).delete()

    return redirect(reverse('tactical:room_edit', args=[room.id]))
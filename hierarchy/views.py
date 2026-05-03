import json
import logging

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import NodeCreateForm
from .models import Node

User = get_user_model()
logger = logging.getLogger(__name__)


def _format_name(user):
    """Return 'F. COGNOME' formatted display name for a user."""
    if user.first_name:
        return f"{user.first_name[0].upper()}. {user.last_name.upper()}"
    return user.last_name.upper()


@login_required
def hierarchy_map(request):
    """
    Render the full-page organisational chart.
    Passes all node data as a JSON array consumed by OrgChart.js on the client.
    Also passes the NodeCreateForm so staff can create nodes via the modal.
    """
    nodes = (
        Node.objects.select_related("leader")
        .prefetch_related("members")
        .order_by("order", "name")
    )

    node_data = []
    for node in nodes:
        members = list(node.members.all())

        leader_name = ""
        leader_rank = ""
        leader_photo = ""
        if node.leader:
            leader_name = _format_name(node.leader)
            leader_rank = node.leader.get_rank_display()
            if node.leader.profile_image:
                leader_photo = node.leader.profile_image.url

        member_list = [
            {
                "id": m.pk,
                "rank": m.get_rank_display(),
                "name": _format_name(m),
                "photo": m.profile_image.url if m.profile_image else "",
            }
            for m in members[:9]
        ]
        member_extra = max(0, len(members) - 9)
        member_ids = [m.pk for m in members]
        member_count = len(members)

        node_data.append(
            {
                "id": node.pk,
                "pid": node.parent_id,
                "node_name": node.name,
                "node_type": node.get_node_type_display(),
                "node_type_key": node.node_type,
                "leader_rank": leader_rank,
                "leader_name": leader_name,
                "leader_photo": leader_photo,
                "leader_id": node.leader_id,
                "order": node.order,
                "members": member_list,
                "member_extra": member_extra,
                "member_ids": member_ids,
                "member_count": member_count,
            }
        )

    form = NodeCreateForm() if request.user.is_staff else None

    return render(
        request,
        "hierarchy/hierarchy_map.html",
        {
            "node_data_json": json.dumps(node_data),
            "current_user_id": request.user.pk,
            "form": form,
        },
    )


@staff_member_required
def node_create(request):
    """Handle POST submission of the NodeCreateForm from the front-end modal."""
    if request.method == "POST":
        form = NodeCreateForm(request.POST)
        if form.is_valid():
            node = form.save()
            logger.info("Staff %s created node '%s' (pk=%s)", request.user, node.name, node.pk)
            return redirect("hierarchy:hierarchy_map")
        # Re-render the map page with form errors so the modal can show them
        nodes = (
            Node.objects.select_related("leader")
            .prefetch_related("members")
            .order_by("order", "name")
        )
        node_data = []
        for node in nodes:
            members = list(node.members.all())
            leader_name = leader_rank = leader_photo = ""
            if node.leader:
                leader_name = _format_name(node.leader)
                leader_rank = node.leader.get_rank_display()
                if node.leader.profile_image:
                    leader_photo = node.leader.profile_image.url
            member_list = [{"rank": m.get_rank_display(), "name": _format_name(m)} for m in members[:5]]
            node_data.append({
                "id": node.pk, "pid": node.parent_id,
                "node_name": node.name, "node_type": node.get_node_type_display(),
                "node_type_key": node.node_type, "leader_rank": leader_rank,
                "leader_name": leader_name, "leader_photo": leader_photo,
                "members": member_list, "member_extra": max(0, len(members) - 5),
            })
        return render(request, "hierarchy/hierarchy_map.html", {
            "node_data_json": json.dumps(node_data),
            "current_user_id": request.user.pk,
            "form": form,
            "open_modal": True,
        })
    return redirect("hierarchy:hierarchy_map")


@staff_member_required
def node_edit(request, pk):
    """Handle POST to edit an existing Node."""
    node = get_object_or_404(Node, pk=pk)
    if request.method == "POST":
        form = NodeCreateForm(request.POST, instance=node)
        if form.is_valid():
            form.save()
            logger.info("Staff %s edited node '%s' (pk=%s)", request.user, node.name, pk)
        else:
            logger.warning("Staff %s submitted invalid edit for node pk=%s: %s", request.user, pk, form.errors)
            messages.error(request, "Ugyldig formular – ændringer blev ikke gemt.")
    return redirect("hierarchy:hierarchy_map")


@staff_member_required
def node_delete(request, pk):
    """Handle POST to delete a Node."""
    if request.method == "POST":
        node = get_object_or_404(Node, pk=pk)
        logger.info("Staff %s deleted node '%s' (pk=%s)", request.user, node.name, pk)
        node.delete()
    return redirect("hierarchy:hierarchy_map")


MEMBER_LIMIT = 9


@staff_member_required
@require_http_methods(["GET", "POST"])
def node_members(request, pk):
    """GET: return JSON list of all active users with membership status.
       POST: update the members of the node."""
    node = get_object_or_404(Node.objects.prefetch_related("members"), pk=pk)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        new_ids = [int(i) for i in data.get("member_ids", [])]
        # Enforce limit
        new_ids = new_ids[:MEMBER_LIMIT]
        node.members.set(User.objects.filter(pk__in=new_ids, is_active=True))
        logger.info("Staff %s updated members of node pk=%s: %s", request.user, pk, new_ids)
        return JsonResponse({"ok": True, "count": node.members.count()})

    # GET — build user list
    current_ids = set(node.members.values_list("pk", flat=True))
    # users in OTHER nodes (exclude current node)
    occupied_ids = set(
        Node.objects.exclude(pk=pk)
        .values_list("members__pk", flat=True)
    ) - {None}

    qs = (
        User.objects.filter(is_active=True)
        .exclude(pk=node.leader_id)
        .order_by("last_name", "first_name")
    )
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(last_name__icontains=q) | qs.filter(first_name__icontains=q)

    total = qs.count()
    users = qs[:100]

    user_list = []
    for u in users:
        user_list.append({
            "id": u.pk,
            "name": _format_name(u),
            "rank": u.get_rank_display(),
            "photo": u.profile_image.url if u.profile_image else "",
            "in_node": u.pk in current_ids,
            "in_other": u.pk in occupied_ids,
        })

    return JsonResponse({
        "users": user_list,
        "current_ids": list(current_ids),
        "limit": MEMBER_LIMIT,
        "total": total,
    })


@staff_member_required
@require_http_methods(["GET", "POST"])
def node_leader(request, pk):
    """GET: return JSON list of users available as leader.
       POST: set the leader of the node."""
    node = get_object_or_404(Node, pk=pk)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        leader_id = data.get("leader_id")
        if leader_id:
            node.leader = get_object_or_404(User, pk=int(leader_id), is_active=True)
        else:
            node.leader = None
        node.save(update_fields=["leader"])
        logger.info("Staff %s set leader of node pk=%s to user pk=%s", request.user, pk, leader_id)
        return JsonResponse({"ok": True})

    # GET — users not already a leader in another node
    taken_leader_ids = set(
        Node.objects.exclude(pk=pk)
        .exclude(leader__isnull=True)
        .values_list("leader_id", flat=True)
    )

    users = (
        User.objects.filter(is_active=True)
        .order_by("last_name", "first_name")
    )

    user_list = []
    for u in users:
        user_list.append({
            "id": u.pk,
            "name": _format_name(u),
            "rank": u.get_rank_display(),
            "photo": u.profile_image.url if u.profile_image else "",
            "is_current": u.pk == node.leader_id,
            "taken": u.pk in taken_leader_ids,
        })

    return JsonResponse({
        "users": user_list,
        "current_leader_id": node.leader_id,
    })

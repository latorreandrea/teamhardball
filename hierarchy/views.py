import json

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import NodeCreateForm
from .models import Node

User = get_user_model()


def _format_name(user):
    """Return 'F. COGNOME' formatted display name for a user."""
    if user.first_name:
        return f"{user.first_name[0]}. {user.last_name.upper()}"
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
                "rank": m.get_rank_display(),
                "name": _format_name(m),
            }
            for m in members[:5]
        ]
        member_extra = max(0, len(members) - 5)
        member_ids = [m.pk for m in members]

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
            form.save()
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
            "form": form,
            "open_modal": True,
        })
    return redirect("hierarchy:hierarchy_map")


@staff_member_required
def node_edit(request, pk):
    """Handle POST to edit an existing Node."""
    node = Node.objects.get(pk=pk)
    if request.method == "POST":
        form = NodeCreateForm(request.POST, instance=node)
        if form.is_valid():
            form.save()
    return redirect("hierarchy:hierarchy_map")


@staff_member_required
def node_delete(request, pk):
    """Handle POST to delete a Node."""
    if request.method == "POST":
        Node.objects.filter(pk=pk).delete()
    return redirect("hierarchy:hierarchy_map")

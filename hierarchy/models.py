from django.conf import settings
from django.db import models


class Node(models.Model):
    """
    Represents a single organisational unit in the club hierarchy.
    Can be the top-level command node or any child unit / patrol.
    Uses a self-referential ForeignKey to build the tree.
    """

    NODE_TYPE_COMMAND = "command"
    NODE_TYPE_UNIT = "unit"
    NODE_TYPE_PATROL = "patrol"

    NODE_TYPE_CHOICES = [
        (NODE_TYPE_COMMAND, "Kommando"),
        (NODE_TYPE_UNIT, "Enhed"),
        (NODE_TYPE_PATROL, "Patrulje"),
    ]

    name = models.CharField("name", max_length=150)
    node_type = models.CharField(
        "type", max_length=20, choices=NODE_TYPE_CHOICES, default=NODE_TYPE_UNIT
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
        verbose_name="parent node",
    )
    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="led_nodes",
        verbose_name="leader",
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="nodes",
        verbose_name="members",
    )
    order = models.PositiveSmallIntegerField(
        "display order",
        default=0,
        help_text="Lower numbers appear first among siblings.",
    )

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "node"
        verbose_name_plural = "nodes"

    def __str__(self):
        return self.name



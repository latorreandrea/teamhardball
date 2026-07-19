from django.conf import settings
from django.db import models


class Room(models.Model):
    """
    A tactical game room created by an admin.
    Represents a single Milsim operation with a defined area of play.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)

    # Area of play — bounding box
    bounds_north = models.FloatField()
    bounds_south = models.FloatField()
    bounds_east = models.FloatField()
    bounds_west = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Platoon(models.Model):
    """A platoon (squad) within a room, led by a Team Leader."""
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='platoons',
    )
    name = models.CharField(max_length=50)
    team_leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='led_platoons',
    )

    class Meta:
        unique_together = ['room', 'name']

    def __str__(self):
        return f"{self.name} ({self.room.name})"


class RoomAssignment(models.Model):
    """Links a user to a room and platoon with a specific role."""
    ROLE_CHOICES = [
        ('team_leader', 'Team Leader'),
        ('member', 'Member'),
    ]

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='assignments',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tactical_assignments',
    )
    platoon = models.ForeignKey(
        Platoon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members',
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='member',
    )

    class Meta:
        unique_together = ['room', 'user']

    def __str__(self):
        return f"{self.user} → {self.room} [{self.role}]"


class SpawnPoint(models.Model):
    """Pre-configured spawn point on the tactical map."""
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='spawn_points',
    )
    name = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"Spawn: {self.name} ({self.room.name})"


class HQPoint(models.Model):
    """Headquarters / base point on the tactical map."""
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='hq_points',
    )
    name = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"HQ: {self.name} ({self.room.name})"
import io

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image as PilImage


MAX_ICON_BYTES = 512 * 1024
MAX_ICON_DIMENSION = 128


def _compress_icon(field_file):
    img = PilImage.open(field_file)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    img.thumbnail((MAX_ICON_DIMENSION, MAX_ICON_DIMENSION), PilImage.LANCZOS)
    output = io.BytesIO()
    img.save(output, format='WEBP', quality=82, optimize=True)
    output.seek(0)
    original_name = field_file.name.rsplit('.', 1)[0]
    return ContentFile(output.read(), name=f'{original_name}.webp')


class AchievementDefinition(models.Model):
    slug = models.SlugField(unique=True, max_length=120, db_index=True, blank=True)
    title = models.CharField(max_length=120)
    info = models.TextField(blank=True, help_text='Hvorfor dette achievement gives.')
    icon = models.ImageField(upload_to="achievement_badges/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "achievement definition"
        verbose_name_plural = "achievement definitions"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        new_icon_uploading = bool(self.icon and hasattr(self.icon, 'file'))
        if self.pk and new_icon_uploading:
            try:
                old = AchievementDefinition.objects.get(pk=self.pk)
                if old.icon and old.icon.name != self.icon.name:
                    old.icon.delete(save=False)
            except AchievementDefinition.DoesNotExist:
                pass

        if new_icon_uploading:
            try:
                self.icon = _compress_icon(self.icon)
            except Exception:
                pass

        super().save(*args, **kwargs)

    def clean(self):
        if self.icon and hasattr(self.icon, 'size') and self.icon.size > MAX_ICON_BYTES:
            raise ValidationError(
                f'Billedet er for stort ({self.icon.size / 1024:.0f} KB). '
                f'Maks tilladt størrelse er {MAX_ICON_BYTES // 1024} KB.'
            )


class UserAchievement(models.Model):
    class Source(models.TextChoices):
        AUTO = "auto", "Automatic"
        MANUAL = "manual", "Manual"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="achievements",
    )
    achievement = models.ForeignKey(
        AchievementDefinition,
        on_delete=models.CASCADE,
        related_name="awards",
    )
    awarded_at = models.DateTimeField(default=timezone.now, db_index=True)
    awarded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="awarded_achievements",
    )
    reason = models.TextField(blank=True)
    source = models.CharField(max_length=10, choices=Source.choices, default=Source.MANUAL)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "achievement"],
                name="unique_user_achievement",
            )
        ]
        ordering = ["-awarded_at"]
        verbose_name = "user achievement"
        verbose_name_plural = "user achievements"

    def __str__(self):
        return f"{self.user} - {self.achievement}"

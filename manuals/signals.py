from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Chapter, Manual


# ── Delete cover image when a Manual is deleted ───────────────────────────────
@receiver(post_delete, sender=Manual)
def delete_manual_cover(sender, instance, **kwargs):
    if instance.cover_image:
        instance.cover_image.delete(save=False)


# ── Delete chapter image when a Chapter is deleted ────────────────────────────
# This fires both for explicit chapter deletes and cascaded deletes
# (when the parent Manual is removed).
@receiver(post_delete, sender=Chapter)
def delete_chapter_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)

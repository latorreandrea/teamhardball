import io

from django.conf import settings
from django.db import models
from PIL import Image as PilImage


def _compress_image(field_file, max_dimension=1200):
    """Resize and convert an uploaded image to WebP, quality 82."""
    img = PilImage.open(field_file)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    img.thumbnail((max_dimension, max_dimension), PilImage.LANCZOS)
    output = io.BytesIO()
    img.save(output, format='WEBP', quality=82, optimize=True)
    output.seek(0)
    from django.core.files.base import ContentFile
    base_name = field_file.name.rsplit('.', 1)[0]
    return ContentFile(output.read(), name=f'{base_name}.webp')


class Equipment(models.Model):
    """A piece of equipment registered by a member and available for borrowing."""

    CATEGORY_AEG         = 'aeg'
    CATEGORY_GBB         = 'gbb'
    CATEGORY_SPRINGER    = 'springer'
    CATEGORY_HPA         = 'hpa'
    CATEGORY_ACCESSORIES = 'accessories'
    CATEGORY_CLOTHING    = 'clothing'

    CATEGORY_CHOICES = [
        (CATEGORY_AEG,         'AEG (Automatisk elektrisk gevær)'),
        (CATEGORY_GBB,         'GBB (Gas Blowback)'),
        (CATEGORY_SPRINGER,    'Molla (Springer)'),
        (CATEGORY_HPA,         'HPA (High Pressure Air)'),
        (CATEGORY_ACCESSORIES, 'Tilbehør'),
        (CATEGORY_CLOTHING,    'Beklædning'),
    ]

    name        = models.CharField(max_length=200)
    image       = models.ImageField(
        upload_to='armoury/',
        blank=True,
        null=True,
        help_text='Billede af udstyret (maks. 5 MB, komprimeres automatisk til WebP).',
    )
    category    = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    owner       = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_equipment',
    )
    description = models.TextField(blank=True)
    borrowed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='borrowed_equipment',
    )
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering     = ['-created_at']
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipment'

    def __str__(self):
        return self.name

    @property
    def is_available(self):
        return self.borrowed_by is None

    def save(self, *args, **kwargs):
        # Compress image only when a new file is being uploaded.
        if self.pk:
            try:
                old_image = Equipment.objects.get(pk=self.pk).image
            except Equipment.DoesNotExist:
                old_image = None
        else:
            old_image = None

        new_image_uploaded = self.image and hasattr(self.image, 'file')
        if new_image_uploaded and self.image != old_image:
            self.image = _compress_image(self.image)

        super().save(*args, **kwargs)

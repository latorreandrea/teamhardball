import io

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from django.utils.text import slugify
from PIL import Image

# Max upload size: 5 MB
MAX_IMAGE_BYTES = 5 * 1024 * 1024
# Longest edge after resize
MAX_IMAGE_DIMENSION = 1200


def _compress_image(field_file):
    """Resize and compress an uploaded image, save as WebP."""
    img = Image.open(field_file)
    # Convert palette/RGBA to RGB for WebP compatibility
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    # Downscale if needed (preserving aspect ratio)
    img.thumbnail((MAX_IMAGE_DIMENSION, MAX_IMAGE_DIMENSION), Image.LANCZOS)
    output = io.BytesIO()
    img.save(output, format='WEBP', quality=82, optimize=True)
    output.seek(0)
    # Rename extension to .webp
    original_name = field_file.name.rsplit('.', 1)[0]
    return ContentFile(output.read(), name=f'{original_name}.webp')


class Post(models.Model):
    """Base model for news posts and blog entries."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='comms_images/', blank=True, null=True)
    seo_description = models.CharField(
        max_length=160,
        blank=True,
        help_text='Text shown in Google search results (max 160 characters).',
    )

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        if self.image and hasattr(self.image, 'size') and self.image.size > MAX_IMAGE_BYTES:
            raise ValidationError(
                f'Billedet er for stort ({self.image.size / 1024 / 1024:.1f} MB). '
                f'Maks tilladt størrelse er {MAX_IMAGE_BYTES // 1024 // 1024} MB.'
            )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        # True only when a freshly uploaded file is attached (InMemoryUploadedFile /
        # TemporaryUploadedFile), not when an existing FieldFile is kept unchanged.
        new_image_uploading = bool(self.image and hasattr(self.image, 'file'))

        # Delete the previous image from storage before saving the new one.
        # This guarantees at most one image per post at all times.
        if self.pk and new_image_uploading:
            try:
                old = Post.objects.get(pk=self.pk)
                if old.image:
                    old.image.delete(save=False)
            except Post.DoesNotExist:
                pass

        # Compress and convert to WebP only for freshly uploaded files.
        if new_image_uploading:
            try:
                self.image = _compress_image(self.image)
            except Exception:
                pass  # Leave original file untouched if compression fails

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Event(models.Model):
    """Specific model for operations and gatherings (events)."""
    related_post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='event_details')
    event_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    max_participants = models.PositiveIntegerField(default=20)

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Attendance',
        related_name='events_joined',
    )

    def __str__(self):
        return f'Event: {self.related_post.title}'


class Attendance(models.Model):
    """Junction table linking users to events (RSVP)."""
    STATUS_CHOICES = [
        ('confirmed', 'Operativo'),
        ('declined', 'Fuori Servizio'),
        ('standby', 'In Stand-by'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='standby')

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f'{self.user} – {self.event} – {self.get_status_display()}'

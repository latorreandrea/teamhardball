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


# The rank values stored in User.rank — mirrored here so we can filter by them.
RANK_CHOICES = [
    ('gen',   'GEN'),
    ('cpt',   'CPT'),
    ('1lt',   '1LT'),
    ('2lt',   '2LT'),
    ('sgt1c', 'SGT 1C'),
    ('ssgt',  'SSGT'),
    ('sgt',   'SGT'),
    ('cpl',   'CPL'),
    ('spc',   'SPC'),
    ('pvt1',  'PVT 1'),
    ('pvt2',  'PVT 2'),
    ('pvt',   'PVT'),
]


class Manual(models.Model):
    """A restricted military-style manual, visible only to authorised ranks."""

    title        = models.CharField(max_length=200)
    description  = models.TextField(blank=True)
    cover_image  = models.ImageField(
        upload_to='manual_covers/',
        blank=True,
        null=True,
        help_text='Forsidebillede (maks. 5 MB, komprimeres automatisk til WebP).',
    )
    created_at   = models.DateTimeField(auto_now_add=True)

    # Which ranks may read this manual — store as a simple comma-separated
    # CharField so we avoid an extra DB table while keeping flexibility.
    allowed_ranks = models.CharField(
        max_length=200,
        help_text=(
            'Kommasepareret liste over rang-koder der må læse manualen, '
            'f.eks. "gen,cpt,1lt". Lad feltet stå tomt for alle.'
        ),
        blank=True,
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Manual'
        verbose_name_plural = 'Manualer'

    def __str__(self):
        return self.title

    def is_accessible_by(self, user):
        """Return True if *user* is allowed to read this manual."""
        if not user.is_authenticated:
            return False
        if not self.allowed_ranks:
            return True   # no restriction → visible to all members
        return user.rank in [r.strip() for r in self.allowed_ranks.split(',')]

    def save(self, *args, **kwargs):
        new_image = self.cover_image and hasattr(self.cover_image, 'file')

        # Replace previous cover image in storage before uploading new one.
        if self.pk and new_image:
            try:
                old = Manual.objects.get(pk=self.pk)
                if old.cover_image:
                    old.cover_image.delete(save=False)
            except Manual.DoesNotExist:
                pass

        if new_image:
            try:
                self.cover_image = _compress_image(self.cover_image)
            except Exception:
                pass

        super().save(*args, **kwargs)


class Chapter(models.Model):
    """A single page / chapter inside a Manual."""

    manual  = models.ForeignKey(Manual, on_delete=models.CASCADE, related_name='chapters')
    title   = models.CharField(max_length=200)
    content = models.TextField(help_text='Supports HTML markup.')
    order   = models.PositiveSmallIntegerField(
        default=0,
        help_text='Laveste tal vises først. Lad stå 0 for automatisk tildeling.',
    )
    image   = models.ImageField(
        upload_to='manual_chapters/',
        blank=True,
        null=True,
        help_text='Valgfrit illustrationsbillede til kapitlet (WebP komprimeres automatisk).',
    )

    class Meta:
        ordering = ['order', 'pk']
        verbose_name = 'Kapitel'
        verbose_name_plural = 'Kapitler'

    def __str__(self):
        return f'{self.manual.title} – {self.order}. {self.title}'

    def save(self, *args, **kwargs):
        # Auto-assign the lowest unused order number when order is 0 (default)
        # and the chapter is new (no pk yet) or order hasn't been manually set.
        if self.order == 0:
            used = set(
                Chapter.objects
                .filter(manual=self.manual)
                .exclude(pk=self.pk)   # exclude self when editing
                .values_list('order', flat=True)
            )
            # Find the lowest positive integer not already taken
            candidate = 1
            while candidate in used:
                candidate += 1
            self.order = candidate

        new_image = self.image and hasattr(self.image, 'file')

        if self.pk and new_image:
            try:
                old = Chapter.objects.get(pk=self.pk)
                if old.image:
                    old.image.delete(save=False)
            except Chapter.DoesNotExist:
                pass

        if new_image:
            try:
                self.image = _compress_image(self.image)
            except Exception:
                pass

        super().save(*args, **kwargs)

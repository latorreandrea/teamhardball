from django import forms
from PIL import Image as PilImage

from .models import Event, Post

# Max upload size enforced at the form layer so the user gets a clear error.
_MAX_IMAGE_MB = 5
_MAX_IMAGE_BYTES = _MAX_IMAGE_MB * 1024 * 1024


def _validate_image_field(image):
    """
    Raise forms.ValidationError if the uploaded image is too large or not a
    valid image file. Called from clean_image() in each form that has an image
    field.
    """
    if not image:
        return image

    # 1. Size check
    if hasattr(image, 'size') and image.size > _MAX_IMAGE_BYTES:
        raise forms.ValidationError(
            f'Billedet er for stort ({image.size / 1024 / 1024:.1f} MB). '
            f'Maks tilladt størrelse er {_MAX_IMAGE_MB} MB.'
        )

    # 2. Verify the file is actually a readable image (catches corrupt files
    #    and files that are not images despite having an image extension).
    try:
        image.seek(0)
        with PilImage.open(image) as img:
            img.load()   # force-decode so truncated files also fail here
        image.seek(0)    # reset pointer so the storage backend can re-read it
    except Exception:
        raise forms.ValidationError(
            'Filen er ikke et gyldigt billede. '
            'Upload venligst en JPG, PNG eller WebP fil.'
        )

    return image


class NewsForm(forms.ModelForm):
    """Form for creating/editing a plain News post (no event details)."""

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'seo_description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titel på nyheden'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Indhold…'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'seo_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kort beskrivelse til Google (max 160 tegn)',
                'maxlength': 160,
            }),
        }
        labels = {
            'title': 'Titel',
            'content': 'Indhold',
            'image': 'Billede (maks. 5 MB – komprimeres automatisk)',
            'seo_description': 'SEO beskrivelse',
        }

    def clean_image(self):
        return _validate_image_field(self.cleaned_data.get('image'))


class EventPostForm(forms.ModelForm):
    """Form for the Post part of an Event."""

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'seo_description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titel på event'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Beskrivelse…'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'seo_description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kort beskrivelse til Google (max 160 tegn)',
                'maxlength': 160,
            }),
        }
        labels = {
            'title': 'Titel',
            'content': 'Beskrivelse',
            'image': 'Billede (maks. 5 MB – komprimeres automatisk)',
            'seo_description': 'SEO beskrivelse',
        }

    def clean_image(self):
        return _validate_image_field(self.cleaned_data.get('image'))


class EventDetailsForm(forms.ModelForm):
    """Form for the Event-specific fields."""

    class Meta:
        model = Event
        fields = ['event_date', 'location', 'max_participants']
        widgets = {
            'event_date': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lokation'}),
            'max_participants': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
        labels = {
            'event_date': 'Dato & tidspunkt',
            'location': 'Lokation',
            'max_participants': 'Maks. deltagere',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-fill datetime-local format for existing instances
        if self.instance and self.instance.event_date:
            self.fields['event_date'].initial = self.instance.event_date.strftime('%Y-%m-%dT%H:%M')

from django import forms

from .models import Event, Post


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

from django import forms
from django.forms import inlineformset_factory

from .models import Chapter, Manual, RANK_CHOICES


class ManualForm(forms.ModelForm):
    """Form for creating / editing a Manual with a rank-selector."""

    # Render allowed_ranks as a multi-select checkbox list.
    allowed_ranks = forms.MultipleChoiceField(
        choices=RANK_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Tilladte rang',
        help_text='Sæt hak ved de ranger der må læse manualen. Lad alle være tomme = alle rang.',
    )

    class Meta:
        model = Manual
        fields = ['title', 'description', 'cover_image', 'allowed_ranks']
        widgets = {
            'title':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Manualens titel'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
        labels = {
            'title':       'Titel',
            'description': 'Beskrivelse',
            'cover_image': 'Forsidebillede (maks. 5 MB)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-populate multi-select from the stored comma-separated string.
        if self.instance and self.instance.allowed_ranks:
            self.fields['allowed_ranks'].initial = [
                r.strip() for r in self.instance.allowed_ranks.split(',')
            ]

    def clean_allowed_ranks(self):
        selected = self.cleaned_data.get('allowed_ranks', [])
        return ','.join(selected)

    def clean_cover_image(self):
        image = self.cleaned_data.get('cover_image')
        if image and hasattr(image, 'size'):
            max_bytes = 5 * 1024 * 1024
            if image.size > max_bytes:
                raise forms.ValidationError(
                    f'Billedet er for stort ({image.size / 1024 / 1024:.1f} MB). '
                    'Maks tilladt størrelse er 5 MB.'
                )
        return image


class ChapterForm(forms.ModelForm):
    """Inline form for a single chapter."""

    class Meta:
        model = Chapter
        fields = ['title', 'content', 'order', 'image']
        widgets = {
            'title':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kapiteloverskrift'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'order':   forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'image':   forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
        labels = {
            'title':   'Titel',
            'content': 'Indhold (HTML tilladt)',
            'order':   'Rækkefølge',
            'image':   'Illustrationsbillede',
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and hasattr(image, 'size'):
            max_bytes = 5 * 1024 * 1024
            if image.size > max_bytes:
                raise forms.ValidationError(
                    f'Billedet er for stort ({image.size / 1024 / 1024:.1f} MB). '
                    'Maks tilladt størrelse er 5 MB.'
                )
        return image


ChapterFormSet = inlineformset_factory(
    Manual,
    Chapter,
    form=ChapterForm,
    extra=0,          # start with 0 extra blank forms; JS adds them dynamically
    can_delete=True,
    max_num=50,
    validate_max=False,
)

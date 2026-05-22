from django import forms

from .models import Equipment


class EquipmentForm(forms.ModelForm):
    """Form for registering or editing a piece of equipment."""

    class Meta:
        model  = Equipment
        fields = ['name', 'image', 'category', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Udstyrets navn',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Beskriv udstyret…',
            }),
        }
        labels = {
            'name':        'Navn',
            'image':       'Billede (maks. 5 MB)',
            'category':    'Kategori',
            'description': 'Beskrivelse',
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and hasattr(image, 'size'):
            max_bytes = 5 * 1024 * 1024
            if image.size > max_bytes:
                raise forms.ValidationError('Billedet må ikke overstige 5 MB.')
        return image

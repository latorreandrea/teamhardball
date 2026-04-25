from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import AchievementDefinition, MAX_ICON_BYTES

User = get_user_model()


class AchievementDefinitionForm(forms.ModelForm):
    icon = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        help_text='Maks 512 KB. Konverteres automatisk til WebP og skaleres til max 128×128 px.',
    )

    class Meta:
        model = AchievementDefinition
        fields = [
            'title',
            'slug',
            'info',
            'icon',
            'is_active',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'info': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_icon(self):
        image = self.cleaned_data.get('icon')
        if image and image.size > MAX_ICON_BYTES:
            raise ValidationError(
                f'Billedet er for stort ({image.size / 1024:.0f} KB). '
                f'Maks tilladt størrelse er {MAX_ICON_BYTES // 1024} KB.'
            )
        return image


class UserAchievementCreateForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_active=True).order_by('last_name', 'first_name'),
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': 8}),
        label='Brugere',
        help_text='Vælg en eller flere brugere, som skal modtage achievement.',
    )
    achievement = forms.ModelChoiceField(
        queryset=AchievementDefinition.objects.filter(is_active=True).order_by('title'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Achievement',
    )
    reason = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label='Begrundelse',
        help_text='Valgfri begrundelse, som vises i brugerens opnåelse.',
    )


class AchievementMembershipForm(forms.Form):
    add_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': 8}),
        label='Tilføj brugere',
        help_text='Vælg en eller flere brugere, der skal have dette achievement.',
    )
    remove_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': 8}),
        label='Fjern brugere',
        help_text='Vælg brugere, der skal fjernes fra dette achievement.',
    )

    def __init__(self, *args, achievement=None, **kwargs):
        super().__init__(*args, **kwargs)
        if achievement is None:
            raise ValueError('Achievement must be provided for membership form.')
        self.fields['add_users'].queryset = User.objects.filter(is_active=True).exclude(achievements=achievement).order_by('last_name', 'first_name')
        self.fields['remove_users'].queryset = User.objects.filter(achievements=achievement).order_by('last_name', 'first_name')

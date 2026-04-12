from django import forms
from .models import JoinRequest


class JoinRequestForm(forms.ModelForm):
    """Form for users to request membership"""
    
    class Meta:
        model = JoinRequest
        fields = ['first_name', 'last_name', 'email', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Indtast dit fornavn'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Indtast dit efternavn'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'din.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+45 12 34 56 78'
            }),
        }
        labels = {
            'first_name': 'Fornavn',
            'last_name': 'Efternavn',
            'email': 'Email',
            'phone': 'Telefonnummer',
        }

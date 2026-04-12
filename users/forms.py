from django import forms
from .models import JoinRequest


class JoinRequestForm(forms.ModelForm):
    """Form for users to request membership"""
    
    class Meta:
        model = JoinRequest
        fields = ['nome', 'cognome', 'email', 'telefono']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Indtast dit fornavn'
            }),
            'cognome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Indtast dit efternavn'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'din.email@example.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+45 12 34 56 78'
            }),
        }
        labels = {
            'nome': 'Fornavn',
            'cognome': 'Efternavn',
            'email': 'Email',
            'telefono': 'Telefonnummer',
        }

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ExpenseRequest, Transaction


class ExpenseRequestForm(forms.ModelForm):
    """Form for members to submit a new spending request."""

    class Meta:
        model = ExpenseRequest
        fields = ['amount', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0.01',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Describe what the expense covers and why it is necessary.'),
            }),
        }


class ExpenseRequestWidget(forms.Select):
    """Custom Select widget that adds data-amount and data-description
    attributes to each <option> for the expense request dropdown."""

    def __init__(self, attrs=None, request_data=None):
        super().__init__(attrs)
        self.request_data = request_data or {}

    def create_option(self, name, value, label, selected, index,
                      subindex=None, attrs=None):
        option = super().create_option(
            name, value, label, selected, index,
            subindex=subindex, attrs=attrs,
        )
        if value:
            pk = str(value)
            if pk in self.request_data:
                data = self.request_data[pk]
                option['attrs']['data-amount'] = data['amount']
                option['attrs']['data-description'] = data['description']
        return option


class TransactionForm(forms.ModelForm):
    """Form for admins to record an income or expense transaction."""

    class Meta:
        model = Transaction
        fields = [
            'entry_type', 'amount', 'description',
            'incurred_by', 'expense_request', 'note',
        ]
        widgets = {
            'entry_type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0.01',
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('E.g. Ammunition purchase, Membership fee...'),
            }),
            'incurred_by': forms.Select(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': _('Internal notes (not visible to members).'),
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show approved expense requests that haven't been linked yet
        approved_qs = ExpenseRequest.objects.filter(
            status=ExpenseRequest.STATUS_APPROVED,
            transactions__isnull=True,
        ).select_related('user').distinct()
        self.fields['expense_request'].queryset = approved_qs

        # Build a lookup dict for the custom widget
        req_data = {}
        for req in approved_qs:
            req_data[str(req.pk)] = {
                'amount': str(req.amount),
                'description': req.description,
            }
        field = self.fields['expense_request']
        field.widget = ExpenseRequestWidget(
            attrs={'class': 'form-control'},
            request_data=req_data,
        )
        # Populate widget choices from the queryset so options are rendered
        field.widget.choices = field.choices

        self.fields['incurred_by'].required = False
        self.fields['expense_request'].required = False
        self.fields['note'].required = False


class AdminExpenseRequestForm(forms.ModelForm):
    """
    Form for admins to process an expense request:
    approve, reject, or request clarification with a message.
    """

    action = forms.ChoiceField(
        choices=[
            ('approve', 'Godkend'),
            ('reject', 'Afvis'),
            ('clarify', 'Anmod om afklaring'),
        ],
        widget=forms.RadioSelect(),
        initial='approve',
    )
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': _('Optional message to the member (required when requesting clarification).'),
        }),
        label=_('Message'),
    )

    class Meta:
        model = ExpenseRequest
        fields = []

    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get('action')
        message = cleaned_data.get('message', '').strip()

        if action == 'clarify' and not message:
            raise forms.ValidationError(
                _('You must provide a message when requesting clarification.')
            )
        return cleaned_data


class ClarificationResponseForm(forms.ModelForm):
    """Form for members to respond to admin clarification requests."""

    class Meta:
        model = ExpenseRequest
        fields = ['admin_response']
        widgets = {
            'admin_response': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Provide additional information as requested by the admin...'),
            }),
        }
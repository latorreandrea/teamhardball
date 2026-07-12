from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class ExpenseRequest(models.Model):
    """
    Spending request submitted by a member.
    Admins can approve, reject, or ask for clarification.
    If approved, the request becomes selectable as a transaction reason.
    """

    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CLARIFICATION = 'clarification_requested'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Afventer'),
        (STATUS_APPROVED, 'Godkendt'),
        (STATUS_REJECTED, 'Afvist'),
        (STATUS_CLARIFICATION, 'Afventer afklaring'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expense_requests',
        verbose_name=_('requested by'),
    )
    amount = models.DecimalField(
        _('amount'),
        max_digits=10,
        decimal_places=2,
    )
    description = models.TextField(
        _('description'),
        help_text='Beskriv hvad udgiften dækker, og hvorfor den er nødvendig.',
    )
    status = models.CharField(
        _('status'),
        max_length=30,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    admin_message = models.TextField(
        _('admin message'),
        blank=True,
        help_text='Besked fra admin (f.eks. anmodning om flere oplysninger).',
    )
    admin_response = models.TextField(
        _('user response'),
        blank=True,
        help_text='Svar fra brugeren på admins besked.',
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    processed_at = models.DateTimeField(_('processed at'), null=True, blank=True)
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_expense_requests',
        verbose_name=_('processed by'),
    )

    class Meta:
        verbose_name = _('expense request')
        verbose_name_plural = _('expense requests')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.get_full_name()} — {self.amount} kr. ({self.get_status_display()})'


class Transaction(models.Model):
    """
    A single income or expense entry recorded by an admin.
    Can optionally reference an approved expense request as the reason.
    """

    ENTRY_INCOME = 'income'
    ENTRY_EXPENSE = 'expense'

    ENTRY_CHOICES = [
        (ENTRY_INCOME, 'Indtægt'),
        (ENTRY_EXPENSE, 'Udgift'),
    ]

    entry_type = models.CharField(
        _('type'),
        max_length=10,
        choices=ENTRY_CHOICES,
    )
    amount = models.DecimalField(
        _('amount'),
        max_digits=10,
        decimal_places=2,
    )
    description = models.CharField(
        _('description'),
        max_length=500,
    )
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recorded_transactions',
        verbose_name=_('recorded by'),
    )
    incurred_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incurred_transactions',
        verbose_name=_('incurred by'),
    )
    expense_request = models.ForeignKey(
        ExpenseRequest,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions',
        verbose_name=_('expense request'),
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    note = models.TextField(_('internal note'), blank=True)

    class Meta:
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')
        ordering = ['-created_at']

    def __str__(self):
        sign = '+' if self.entry_type == self.ENTRY_INCOME else '−'
        return f'{sign}{self.amount} kr. — {self.description}'


class FinanceViewPermission(models.Model):
    """
    Grants a non-staff user permission to view the finances section.
    Managed by admins through a dedicated UI.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='finance_permission',
        verbose_name=_('user'),
    )
    granted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='granted_finance_permissions',
        verbose_name=_('granted by'),
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('finance view permission')
        verbose_name_plural = _('finance view permissions')

    def __str__(self):
        return f'Finance access: {self.user.get_full_name()}'
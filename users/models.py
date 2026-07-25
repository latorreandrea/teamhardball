import uuid
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string


class UserManager(BaseUserManager):
    """Custom user manager that uses email instead of username"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user"""
        if not email:
            raise ValueError(_('The email address is required'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model for N.S.O.G.
    Uses email as authentication field instead of username.
    """
    
    RANK_CHOICES = [
        ('gen', 'GEN'),
        ('cpt', 'CPT'),
        ('1lt', '1LT'),
        ('2lt', '2LT'),
        ('sgt1c', 'SGT 1C'),
        ('ssgt', 'SSGT'),
        ('sgt', 'SGT'),
        ('cpl', 'CPL'),
        ('spc', 'SPC'),
        ('pvt1', 'PVT 1'),
        ('pvt2', 'PVT 2'),
        ('pvt', 'PVT'),
    ]

    RANK_ORDER = ['gen', 'cpt', '1lt', '2lt', 'sgt1c', 'ssgt', 'sgt', 'cpl', 'spc', 'pvt1', 'pvt2', 'pvt']
    
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    rank = models.CharField(_('rank'), max_length=20, choices=RANK_CHOICES, default='pvt')
    nationality = models.CharField(_('nationality'), max_length=3, blank=True, help_text='ISO code (e.g. DNK, ITA)')
    residence = models.CharField(_('place of residence'), max_length=255, blank=True)
    nickname = models.CharField(_('nickname'), max_length=100, blank=True)
    info = models.TextField(_('info'), blank=True)
    bio = models.TextField(_('bio'), max_length=500, blank=True)
    phone = models.CharField(_('phone number'), max_length=30, blank=True)
    profile_image = models.ImageField(_('profile image'), upload_to='profiles/', blank=True, null=True)
    
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.get_rank_display()} {self.last_name} - {self.email}"
    
    def get_full_name(self):
        """Return the user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    def get_short_name(self):
        """Return the user's short name"""
        return self.first_name


class JoinRequest(models.Model):
    """
    Model for membership join requests from potential new members.
    Admins can approve or reject these requests.
    """
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    # Request information
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'))
    phone = models.CharField(_('phone number'), max_length=20)
    
    # Status tracking
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    processed_at = models.DateTimeField(_('processed at'), null=True, blank=True)
    processed_by = models.ForeignKey(
        'User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='processed_requests',
        verbose_name=_('processed by')
    )
    
    # Rejection reason (if applicable)
    rejection_reason = models.TextField(_('rejection reason'), blank=True)
    
    # Generated password for approved users
    generated_password = models.CharField(_('generated password'), max_length=128, blank=True)
    
    class Meta:
        verbose_name = _('join request')
        verbose_name_plural = _('join requests')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_status_display()}"
    
    def generate_password(self):
        """Generate a random password for the new user"""
        # Generate a secure random password (12 characters)
        password = get_random_string(length=12)
        self.generated_password = password
        return password


class PendingVerificationManager(models.Manager):
    """
    Custom manager that automatically deletes expired verification records
    before every query. Guarantees no expired rows linger beyond 24h.
    """

    def get_queryset(self):
        try:
            super().get_queryset().filter(expires_at__lt=timezone.now()).delete()
        except Exception:
            pass
        return super().get_queryset()

    def expired(self):
        return super().get_queryset().filter(expires_at__lt=timezone.now())


class PendingVerification(models.Model):
    """
    Temporary storage for join request data before email verification.
    Once the user clicks the confirmation link, a JoinRequest is created
    and this record is deleted.
    """

    token = models.UUIDField(
        _('verification token'), primary_key=True, default=uuid.uuid4, editable=False
    )
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'))
    phone = models.CharField(_('phone number'), max_length=20)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    expires_at = models.DateTimeField(_('expires at'))

    objects = PendingVerificationManager()

    class Meta:
        verbose_name = _('pending verification')
        verbose_name_plural = _('pending verifications')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.first_name} {self.last_name} – {self.email} (expires {self.expires_at:%Y-%m-%d %H:%M})'

    @classmethod
    def create_verification(cls, first_name, last_name, email, phone):
        """Create a verification record, clearing any existing ones for this email first."""
        # Delete any existing verification (scaduti or not) for this email
        cls.objects.filter(email=email).delete()
        obj = cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            expires_at=timezone.now() + timedelta(hours=24),
        )
        obj.save()
        return obj

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at


class RankIcon(models.Model):
    """One rank insignia image per rank, stored in the 'ranks/' media folder."""

    rank = models.CharField(
        _('rank'),
        max_length=20,
        choices=User.RANK_CHOICES,
        unique=True,
    )
    icon = models.ImageField(
        _('icon'),
        upload_to='ranks/',
        help_text='Rank insignia image (95×170 px WebP).',
    )

    class Meta:
        verbose_name = _('rank icon')
        verbose_name_plural = _('rank icons')
        ordering = ['rank']

    def __str__(self):
        return f'Icon – {self.get_rank_display()}'

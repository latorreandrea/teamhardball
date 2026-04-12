from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
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
        ('recruit', 'Recruit'),
        ('private', 'Private'),
        ('corporal', 'Corporal'),
        ('sergeant', 'Sergeant'),
        ('lieutenant', 'Lieutenant'),
        ('captain', 'Captain'),
        ('major', 'Major'),
        ('colonel', 'Colonel'),
        ('general', 'General'),
    ]
    
    email = models.EmailField(_('email address'), unique=True)
    nome = models.CharField(_('nome'), max_length=150)
    cognome = models.CharField(_('cognome'), max_length=150)
    rango = models.CharField(_('rango'), max_length=20, choices=RANK_CHOICES, default='recruit')
    nazionalita = models.CharField(_('nazionalità'), max_length=3, blank=True, help_text='Codice ISO (es. DNK, ITA)')
    luogo_residenza = models.CharField(_('luogo di residenza'), max_length=255, blank=True)
    nickname = models.CharField(_('nickname'), max_length=100, blank=True)
    info = models.TextField(_('info'), blank=True)
    
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'cognome']
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['cognome', 'nome']
    
    def __str__(self):
        return f"{self.get_rango_display()} {self.cognome} - {self.email}"
    
    def get_full_name(self):
        """Return the user's full name"""
        return f"{self.nome} {self.cognome}"
    
    def get_short_name(self):
        """Return the user's short name"""
        return self.nome


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
    nome = models.CharField(_('first name'), max_length=150)
    cognome = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'))
    telefono = models.CharField(_('phone number'), max_length=20)
    
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
        return f"{self.nome} {self.cognome} - {self.get_status_display()}"
    
    def generate_password(self):
        """Generate a random password for the new user"""
        # Generate a secure random password (12 characters)
        password = get_random_string(length=12)
        self.generated_password = password
        return password

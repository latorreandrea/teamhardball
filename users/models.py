from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Manager personalizzato per il modello User che usa email invece di username"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Crea e salva un utente normale"""
        if not email:
            raise ValueError(_('L\'indirizzo email è obbligatorio'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Crea e salva un superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Il superuser deve avere is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Il superuser deve avere is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Modello User personalizzato per N.S.O.G.
    Usa email come campo di autenticazione invece di username.
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
        """Ritorna il nome completo dell'utente"""
        return f"{self.nome} {self.cognome}"
    
    def get_short_name(self):
        """Ritorna il nome breve dell'utente"""
        return self.nome

"""
Script per creare il superuser admin
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamhardball.settings')
django.setup()

from users.models import User

# Parametri superuser
EMAIL = 'nsogcip@gmail.com'
PASSWORD = 'Tu@$orell4'
NOME = 'Admin'
COGNOME = 'N.S.O.G.'
RANGO = 'general'

# Controlla se l'utente esiste già
if User.objects.filter(email=EMAIL).exists():
    print(f"L'utente con email {EMAIL} esiste già!")
    user = User.objects.get(email=EMAIL)
    print(f"Aggiorno la password...")
    user.set_password(PASSWORD)
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()
    print(f"Password aggiornata per {user.email}")
else:
    # Crea il superuser
    user = User.objects.create_superuser(
        email=EMAIL,
        password=PASSWORD,
        nome=NOME,
        cognome=COGNOME,
        rango=RANGO
    )
    print(f"Superuser creato con successo!")
    print(f"Email: {user.email}")
    print(f"Nome: {user.get_full_name()}")
    print(f"Rango: {user.get_rango_display()}")

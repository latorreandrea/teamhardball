"""
Script to create the admin superuser
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamhardball.settings')
django.setup()

from users.models import User

# Superuser parameters
EMAIL = 'nsogcip@gmail.com'
PASSWORD = 'Tu@$orell4'
FIRST_NAME = 'Admin'
LAST_NAME = 'N.S.O.G.'
RANK = 'general'

# Check if user already exists
if User.objects.filter(email=EMAIL).exists():
    print(f"User with email {EMAIL} already exists!")
    user = User.objects.get(email=EMAIL)
    print(f"Updating password...")
    user.set_password(PASSWORD)
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()
    print(f"Password updated for {user.email}")
else:
    # Create the superuser
    user = User.objects.create_superuser(
        email=EMAIL,
        password=PASSWORD,
        first_name=FIRST_NAME,
        last_name=LAST_NAME,
        rank=RANK
    )
    print(f"Superuser created successfully!")
    print(f"Email: {user.email}")
    print(f"Name: {user.get_full_name()}")
    print(f"Rank: {user.get_rango_display()}")

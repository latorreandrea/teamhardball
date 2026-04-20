"""
Script to create the admin superuser.
Credentials are read from environment variables — never hardcode them here.

Required env vars:
  ADMIN_EMAIL     — superuser email address
  ADMIN_PASSWORD  — superuser password
  ADMIN_FIRST     — first name (default: Admin)
  ADMIN_LAST      — last name  (default: N.S.O.G.)
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teamhardball.settings')
django.setup()

from users.models import User

EMAIL      = os.environ.get('ADMIN_EMAIL', '')
PASSWORD   = os.environ.get('ADMIN_PASSWORD', '')
FIRST_NAME = os.environ.get('ADMIN_FIRST', 'Admin')
LAST_NAME  = os.environ.get('ADMIN_LAST', 'N.S.O.G.')

if not EMAIL or not PASSWORD:
    print("ERROR: ADMIN_EMAIL and ADMIN_PASSWORD environment variables must be set.")
    sys.exit(1)

if User.objects.filter(email=EMAIL).exists():
    print(f"User {EMAIL} already exists — updating password and permissions.")
    user = User.objects.get(email=EMAIL)
    user.set_password(PASSWORD)
    user.is_staff = True
    user.is_superuser = True
    user.is_active = True
    user.save()
    print("Done.")
else:
    user = User.objects.create_superuser(
        email=EMAIL,
        password=PASSWORD,
        first_name=FIRST_NAME,
        last_name=LAST_NAME,
        rank='gen',
    )
    print(f"Superuser created: {user.email} ({user.get_rank_display()} {user.get_full_name()})")

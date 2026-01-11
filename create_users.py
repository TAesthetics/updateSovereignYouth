#!/usr/bin/env python3
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cyberenigma_web.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone

# Create users with secure passwords
users = [
    {
        'username': 'terence',
        'email': 'terence@cyberenigma.dev',
        'password': 'S0v3r31gnY0uth2025!',
        'first_name': 'Terence',
        'last_name': 'Nwaeke'
    },
    {
        'username': 'flora',
        'email': 'flora@cyberenigma.dev',
        'password': 'Y0uthL34d3rFl0ra!',
        'first_name': 'Flora',
        'last_name': 'Kohlbacher'
    },
    {
        'username': 'phillip',
        'email': 'phillip@cyberenigma.dev',
        'password': 'Ph1ll1pS0v3r31gn!',
        'first_name': 'Phillip',
        'last_name': 'Auber'
    },
    {
        'username': 'jovan',
        'email': 'jovan@cyberenigma.dev',
        'password': 'J0v4nC0achY0uth!',
        'first_name': 'Jovan',
        'last_name': 'Jovanovic'
    }
]

for user_data in users:
    if not User.objects.filter(username=user_data['username']).exists():
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            is_staff=True,
            is_active=True
        )
        print(f"Created user: {user_data['username']}")
    else:
        print(f"User {user_data['username']} already exists")

print("Done!")

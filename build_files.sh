#!/bin/bash

# Collect static files
python3 manage.py collectstatic --noinput

# Run database migrations
python3 manage.py migrate --noinput

# Create superuser from environment variables
python3 -c "
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lgea_portal.settings')
django.setup()
from django.contrib.auth.models import User
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@lgeaschool.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '')
if password and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superuser {username} created successfully')
else:
    print(f'Superuser {username} already exists or no password set')
"

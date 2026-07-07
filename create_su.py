from django.contrib.auth.models import User
from accounts.models import UserProfile

username = 'admin'
password = 'adminpassword123'
email = 'admin@example.com'

if not User.objects.filter(username=username).exists():
    user = User.objects.create_superuser(username, email, password)
    UserProfile.objects.get_or_create(user=user, defaults={'role': 'admin'})
    print(f"Success: Superuser '{username}' created with password '{password}'")
else:
    print(f"Info: Superuser '{username}' already exists.")

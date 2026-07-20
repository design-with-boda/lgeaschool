import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lgea_portal.settings')
application = get_wsgi_application()
app = application

# Automatically run migrations and create/update superuser on startup
try:
    from django.core.management import call_command
    call_command('migrate', interactive=False)
    
    from django.contrib.auth.models import User
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@lgeaschool.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '')
    
    if password:
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            print(f"Superuser {username} created.")
        else:
            u = User.objects.get(username=username)
            u.set_password(password)
            u.save()
            print(f"Superuser {username} password updated.")
except Exception as e:
    print("Startup setup failed:", e)

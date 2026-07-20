"""
URL Configuration for lgea_portal
L.G.E.A STAFF SCHOOL, KEFFI NASARAWA STATE
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

admin.site.site_header = "L.G.E.A Staff School Administration"
admin.site.site_title = "LGEA Portal Admin"
admin.site.index_title = "School Management System"

from django.http import HttpResponse
from django.core.management import call_command
import os

def setup_database(request):
    try:
        # 1. Run migrations
        call_command('migrate', interactive=False)
        
        # 2. Create superuser
        from django.contrib.auth.models import User
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@lgeaschool.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'Lupinsway@177')
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            return HttpResponse(f"SUCCESS: Migrations ran and superuser '{username}' created!")
        else:
            u = User.objects.get(username=username)
            u.set_password(password)
            u.save()
            return HttpResponse(f"SUCCESS: Migrations ran and superuser '{username}' password updated!")
    except Exception as e:
        return HttpResponse(f"ERROR: {str(e)}", status=500)

urlpatterns = [
    path('setup-db/', setup_database),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('students/', include('students.urls')),
    path('teachers/', include('teachers.urls')),
    path('academics/', include('academics.urls')),
    path('news/', include('news.urls')),
    path('gallery/', include('gallery.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from .models import AdminProfile


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'role', 'phone_number', 'date_created']
    search_fields = ['user__username', 'full_name', 'phone_number']

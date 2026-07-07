from django.contrib import admin
from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'position', 'qualification', 'phone', 'is_management', 'is_teaching', 'is_active']
    list_filter = ['qualification', 'is_management', 'is_teaching', 'is_active']
    search_fields = ['first_name', 'last_name', 'email', 'position']
    list_editable = ['is_active', 'is_management', 'is_teaching']
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'middle_name', 'last_name', 'profile_image', 'bio', 'user')
        }),
        ('Professional Information', {
            'fields': ('position', 'department', 'qualification', 'specialization', 'date_joined')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email')
        }),
        ('Status & Display', {
            'fields': ('is_active', 'is_management', 'is_teaching', 'order')
        }),
    )

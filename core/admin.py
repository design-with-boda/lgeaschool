from django.contrib import admin
from .models import SchoolInfo, Announcement, ContactMessage, AdmissionInquiry, SchoolDocument, SchoolEvent


@admin.register(SchoolInfo)
class SchoolInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'tagline', 'established_year', 'logo', 'hero_image')
        }),
        ('Contact Details', {
            'fields': ('address', 'phone', 'email', 'website')
        }),
        ('School Profile', {
            'fields': ('about', 'vision', 'mission')
        }),
        ('Social Media', {
            'fields': ('facebook', 'twitter', 'youtube')
        }),
    )


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'is_active', 'created_at', 'expires_at']
    list_filter = ['priority', 'is_active']
    search_fields = ['title', 'content']
    list_editable = ['is_active']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read']
    search_fields = ['name', 'email', 'subject']
    list_editable = ['is_read']
    readonly_fields = ['created_at']


@admin.register(AdmissionInquiry)
class AdmissionInquiryAdmin(admin.ModelAdmin):
    list_display = ['child_name', 'class_applying', 'parent_name', 'parent_phone', 'status', 'created_at']
    list_filter = ['status', 'class_applying', 'gender']
    search_fields = ['child_name', 'parent_name', 'parent_phone']
    list_editable = ['status']


@admin.register(SchoolDocument)
class SchoolDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_public', 'uploaded_at']
    list_filter = ['category', 'is_public']
    search_fields = ['title']


@admin.register(SchoolEvent)
class SchoolEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'location', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title']
    list_editable = ['is_active']

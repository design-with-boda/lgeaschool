from django.contrib import admin
from .models import Student, Attendance


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'full_name', 'current_class', 'gender', 'parent_name', 'parent_phone', 'is_active']
    list_filter = ['current_class', 'gender', 'is_active']
    search_fields = ['first_name', 'last_name', 'student_id', 'parent_name']
    list_editable = ['is_active']
    readonly_fields = ['student_id', 'admission_date']
    fieldsets = (
        ('Student Information', {
            'fields': ('student_id', 'first_name', 'middle_name', 'last_name', 'gender',
                       'date_of_birth', 'current_class', 'passport_photo', 'blood_group',
                       'medical_notes', 'is_active', 'user')
        }),
        ('Parent / Guardian Information', {
            'fields': ('parent_name', 'parent_phone', 'parent_email', 'parent_occupation',
                       'home_address', 'relationship')
        }),
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'status', 'recorded_by']
    list_filter = ['status', 'date', 'student__current_class']
    search_fields = ['student__first_name', 'student__last_name']
    date_hierarchy = 'date'

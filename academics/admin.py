from django.contrib import admin
from .models import Subject, AcademicSession, Result, LearningMaterial


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'class_level', 'teacher', 'is_active']
    list_filter = ['class_level', 'is_active']
    search_fields = ['name', 'code']


@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ['session', 'term', 'start_date', 'end_date', 'is_current']
    list_editable = ['is_current']


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'session', 'ca1_score', 'ca2_score',
                    'exam_score', 'total_score', 'grade']
    list_filter = ['session', 'subject__class_level', 'grade']
    search_fields = ['student__first_name', 'student__last_name', 'student__student_id']
    readonly_fields = ['grade']

    def total_score(self, obj):
        return obj.total_score
    total_score.short_description = 'Total'


@admin.register(LearningMaterial)
class LearningMaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'material_type', 'uploaded_by', 'is_public', 'uploaded_at']
    list_filter = ['material_type', 'is_public']
    search_fields = ['title']

from django.db import models
from students.models import Student, CLASS_CHOICES
from teachers.models import Teacher


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    class_level = models.CharField(max_length=20, choices=CLASS_CHOICES)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='subjects')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['class_level', 'name']
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return f"{self.name} ({self.class_level})"


class AcademicSession(models.Model):
    TERM_CHOICES = [
        ('First', 'First Term'),
        ('Second', 'Second Term'),
        ('Third', 'Third Term'),
    ]
    session = models.CharField(max_length=20, help_text="e.g. 2023/2024")
    term = models.CharField(max_length=10, choices=TERM_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        unique_together = ['session', 'term']
        ordering = ['-session', 'term']
        verbose_name = "Academic Session"
        verbose_name_plural = "Academic Sessions"

    def __str__(self):
        return f"{self.session} - {self.term} Term"

    def save(self, *args, **kwargs):
        if self.is_current:
            AcademicSession.objects.exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)


class Result(models.Model):
    GRADE_CHOICES = [
        ('A', 'A - Excellent (80-100)'),
        ('B', 'B - Very Good (70-79)'),
        ('C', 'C - Good (60-69)'),
        ('D', 'D - Pass (50-59)'),
        ('E', 'E - Below Average (40-49)'),
        ('F', 'F - Fail (0-39)'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='results')
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name='results')
    ca1_score = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="CA 1 (10)")
    ca2_score = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="CA 2 (10)")
    exam_score = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Exam (60)")
    assignment_score = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Assignment (10)")
    practical_score = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Practical (10)")
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True)
    remarks = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'subject', 'session']
        ordering = ['student', 'subject']
        verbose_name = "Student Result"
        verbose_name_plural = "Student Results"

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.session}"

    @property
    def total_score(self):
        return self.ca1_score + self.ca2_score + self.exam_score + self.assignment_score + self.practical_score

    @property
    def computed_grade(self):
        total = float(self.total_score)
        if total >= 80:
            return 'A'
        elif total >= 70:
            return 'B'
        elif total >= 60:
            return 'C'
        elif total >= 50:
            return 'D'
        elif total >= 40:
            return 'E'
        return 'F'

    def save(self, *args, **kwargs):
        self.grade = self.computed_grade
        super().save(*args, **kwargs)


class LearningMaterial(models.Model):
    TYPE_CHOICES = [
        ('note', 'Class Note'),
        ('assignment', 'Assignment'),
        ('exercise', 'Exercise'),
        ('scheme', 'Scheme of Work'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='materials')
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, related_name='materials')
    material_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='note')
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='materials/', blank=True, null=True)
    uploaded_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    is_public = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Learning Material"
        verbose_name_plural = "Learning Materials"

    def __str__(self):
        return f"{self.title} - {self.subject}"

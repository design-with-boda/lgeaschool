from django.db import models
from django.contrib.auth.models import User


CLASS_CHOICES = [
    ('Nursery 1', 'Nursery 1'),
    ('Nursery 2', 'Nursery 2'),
    ('Primary 1', 'Primary 1'),
    ('Primary 2', 'Primary 2'),
    ('Primary 3', 'Primary 3'),
    ('Primary 4', 'Primary 4'),
    ('Primary 5', 'Primary 5'),
    ('Primary 6', 'Primary 6'),
]

GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    current_class = models.CharField(max_length=20, choices=CLASS_CHOICES)
    passport_photo = models.ImageField(upload_to='students/', blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True)
    medical_notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    admission_date = models.DateField(auto_now_add=True)

    # Parent / Guardian info
    parent_name = models.CharField(max_length=100)
    parent_phone = models.CharField(max_length=20)
    parent_email = models.EmailField(blank=True)
    parent_occupation = models.CharField(max_length=100, blank=True)
    home_address = models.TextField()
    relationship = models.CharField(max_length=50, default="Parent")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['current_class', 'last_name']
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

    @property
    def full_name(self):
        parts = [self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.last_name)
        return ' '.join(parts)

    def save(self, *args, **kwargs):
        if not self.student_id:
            import datetime
            year = datetime.date.today().year
            count = Student.objects.filter(
                admission_date__year=year
            ).count() + 1
            self.student_id = f"LGEA/{year}/{count:04d}"
        super().save(*args, **kwargs)


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    remarks = models.CharField(max_length=200, blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'date']
        ordering = ['-date']
        verbose_name = "Attendance Record"
        verbose_name_plural = "Attendance Records"

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"

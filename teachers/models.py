from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    QUALIFICATION_CHOICES = [
        ('NCE', 'NCE'),
        ('B.Ed', 'B.Ed'),
        ('B.Sc', 'B.Sc'),
        ('M.Ed', 'M.Ed'),
        ('M.Sc', 'M.Sc'),
        ('Ph.D', 'Ph.D'),
        ('Other', 'Other'),
    ]
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='teacher_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=200, default="Class Teacher")
    department = models.CharField(max_length=100, blank=True)
    qualification = models.CharField(max_length=20, choices=QUALIFICATION_CHOICES, default='NCE')
    specialization = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    profile_image = models.ImageField(upload_to='teachers/', blank=True, null=True)
    bio = models.TextField(blank=True)
    date_joined = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_management = models.BooleanField(default=False, help_text="Is part of management team")
    is_teaching = models.BooleanField(default=True, help_text="Is a teaching staff member")
    order = models.IntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'last_name']
        verbose_name = "Teacher / Staff"
        verbose_name_plural = "Teachers / Staff"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        parts = [self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.last_name)
        return ' '.join(parts)

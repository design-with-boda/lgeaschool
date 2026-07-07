from django.db import models


class SchoolInfo(models.Model):
    """Stores core school information displayed site-wide."""
    name = models.CharField(max_length=200, default="L.G.E.A STAFF SCHOOL, KEFFI")
    tagline = models.CharField(max_length=300, blank=True, default="Nurturing Excellence in Every Child")
    address = models.TextField(default="Keffi, Nasarawa State, Nigeria")
    phone = models.CharField(max_length=20, blank=True, default="+234 000 000 0000")
    email = models.EmailField(blank=True, default="info@lgeastaffschoolkeffi.edu.ng")
    website = models.URLField(blank=True)
    about = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    established_year = models.CharField(max_length=10, blank=True, default="1985")
    logo = models.ImageField(upload_to='school/', blank=True, null=True)
    hero_image = models.ImageField(upload_to='school/', blank=True, null=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "School Information"
        verbose_name_plural = "School Information"

    def __str__(self):
        return self.name

    @classmethod
    def get_info(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Announcement(models.Model):
    """School announcements for the homepage slider."""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    """Stores messages from the contact form."""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.subject}"


class AdmissionInquiry(models.Model):
    """Online admission inquiry form submissions."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    child_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    class_applying = models.CharField(max_length=50)
    parent_name = models.CharField(max_length=100)
    parent_phone = models.CharField(max_length=20)
    parent_email = models.EmailField(blank=True)
    address = models.TextField()
    additional_info = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Admission Inquiry"
        verbose_name_plural = "Admission Inquiries"

    def __str__(self):
        return f"{self.child_name} - {self.class_applying}"


class SchoolDocument(models.Model):
    """Downloadable school documents."""
    CATEGORY_CHOICES = [
        ('calendar', 'Academic Calendar'),
        ('timetable', 'Timetable'),
        ('form', 'Forms'),
        ('policy', 'Policy'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    is_public = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "School Document"
        verbose_name_plural = "School Documents"

    def __str__(self):
        return self.title


class SchoolEvent(models.Model):
    """School events calendar."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_date']
        verbose_name = "School Event"
        verbose_name_plural = "School Events"

    def __str__(self):
        return self.title

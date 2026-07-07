from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import SchoolInfo, Announcement, SchoolEvent, SchoolDocument
from .forms import ContactForm, AdmissionInquiryForm
from news.models import NewsPost
from gallery.models import GalleryImage
from teachers.models import Teacher
from students.models import Student


def home(request):
    info = SchoolInfo.get_info()
    latest_news = NewsPost.objects.filter(is_published=True).order_by('-published_at')[:3]
    announcements = Announcement.objects.filter(is_active=True)[:6]
    upcoming_events = SchoolEvent.objects.filter(
        is_active=True, start_date__gte=timezone.now().date()
    ).order_by('start_date')[:4]
    gallery_featured = GalleryImage.objects.filter(is_featured=True)[:6]
    teachers_count = Teacher.objects.filter(is_active=True).count()
    students_count = Student.objects.filter(is_active=True).count()

    context = {
        'info': info,
        'latest_news': latest_news,
        'announcements': announcements,
        'upcoming_events': upcoming_events,
        'gallery_featured': gallery_featured,
        'teachers_count': teachers_count,
        'students_count': students_count,
    }
    return render(request, 'core/home.html', context)


def about(request):
    info = SchoolInfo.get_info()
    management_team = Teacher.objects.filter(
        is_active=True, is_management=True
    ).order_by('order')
    return render(request, 'core/about.html', {'info': info, 'management_team': management_team})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
            return redirect('core:contact')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})


def admission(request):
    if request.method == 'POST':
        form = AdmissionInquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your admission inquiry has been submitted! We will contact you shortly.')
            return redirect('core:admission')
    else:
        form = AdmissionInquiryForm()
    return render(request, 'core/admission.html', {'form': form})


def administration(request):
    head_teacher = Teacher.objects.filter(is_active=True, position__icontains='head').first()
    management = Teacher.objects.filter(is_active=True, is_management=True).order_by('order')
    teaching_staff = Teacher.objects.filter(is_active=True, is_teaching=True, is_management=False).order_by('last_name')
    non_teaching = Teacher.objects.filter(is_active=True, is_teaching=False).order_by('last_name')
    return render(request, 'core/administration.html', {
        'head_teacher': head_teacher,
        'management': management,
        'teaching_staff': teaching_staff,
        'non_teaching': non_teaching,
    })


def documents(request):
    docs = SchoolDocument.objects.filter(is_public=True).order_by('category', '-uploaded_at')
    return render(request, 'core/documents.html', {'docs': docs})


def events(request):
    upcoming = SchoolEvent.objects.filter(
        is_active=True, start_date__gte=timezone.now().date()
    ).order_by('start_date')
    past = SchoolEvent.objects.filter(
        is_active=True, start_date__lt=timezone.now().date()
    ).order_by('-start_date')[:6]
    return render(request, 'core/events.html', {'upcoming': upcoming, 'past': past})

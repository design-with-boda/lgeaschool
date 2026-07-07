from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
from .decorators import admin_required, teacher_required
from students.models import Student
from teachers.models import Teacher
from academics.models import Result, AcademicSession


# ─── helpers ───────────────────────────────────────────────────────────────────

def _get_profile(user):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile

def _is_admin(user, profile):
    return user.is_superuser or user.is_staff or profile.role == 'admin'

def _is_teacher(user, profile):
    return profile.role == 'teacher'

def _is_student(user, profile):
    return profile.role == 'student'


# ─── Login ─────────────────────────────────────────────────────────────────────

def login_portal(request):
    """Landing page that asks users to select their role portal."""
    if request.user.is_authenticated:
        return redirect('accounts:my_dashboard')
    return render(request, 'accounts/login_portal.html')


def login_role(request, role):
    """Role-specific login view that verifies the user actually has the requested role."""
    if request.user.is_authenticated:
        return redirect('accounts:my_dashboard')

    valid_roles = ['staff', 'student', 'parent']
    if role not in valid_roles:
        return redirect('accounts:login')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            profile = _get_profile(user)

            # Validate that the user's role matches the chosen portal
            is_valid_role = False
            if role == 'staff' and (user.is_superuser or user.is_staff or profile.role in ['admin', 'teacher']):
                is_valid_role = True
            elif role == 'student' and profile.role == 'student':
                is_valid_role = True
            elif role == 'parent' and profile.role == 'parent':
                is_valid_role = True

            if is_valid_role:
                login(request, user)
                if request.POST.get('remember_me'):
                    request.session.set_expiry(1209600)  # 2 weeks
                else:
                    request.session.set_expiry(0)        # browser session
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                return redirect('accounts:my_dashboard')
            else:
                messages.error(
                    request,
                    f'This account does not have {role} privileges. '
                    f'Please select the correct portal.'
                )
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form, 'role': role})


# ─── Logout ────────────────────────────────────────────────────────────────────

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('accounts:login')


# ─── Dashboard Dispatcher ──────────────────────────────────────────────────────

@login_required(login_url='/accounts/login/')
def my_dashboard(request):
    """
    Thin dispatcher: redirects each user to their role-specific dashboard URL.
    This is the safe generic entry-point used by LOGIN_REDIRECT_URL.
    """
    user = request.user
    profile = _get_profile(user)

    if _is_admin(user, profile):
        return redirect('accounts:admin_dashboard')
    elif _is_teacher(user, profile):
        return redirect('accounts:teacher_dashboard')
    elif _is_student(user, profile):
        return redirect('accounts:student_dashboard')
    else:
        messages.error(request, 'Your account has no assigned role. Please contact the administrator.')
        logout(request)
        return redirect('accounts:login')


# ─── Admin Dashboard ───────────────────────────────────────────────────────────

@admin_required
def admin_dashboard(request):
    """
    Admin-only dashboard. Protected by @admin_required — any non-admin
    who tries to access /accounts/admin-dashboard/ is denied and redirected.
    """
    from core.models import ContactMessage, AdmissionInquiry

    user = request.user
    profile = _get_profile(user)

    classes = ['Nursery 1', 'Nursery 2', 'Primary 1', 'Primary 2',
               'Primary 3', 'Primary 4', 'Primary 5', 'Primary 6']
    students_by_class = [
        {'class': cls, 'count': Student.objects.filter(current_class=cls, is_active=True).count()}
        for cls in classes
    ]
    max_count = max((item['count'] for item in students_by_class), default=1) or 1

    context = {
        'profile': profile,
        'role': 'admin',
        'total_students': Student.objects.filter(is_active=True).count(),
        'total_teachers': Teacher.objects.filter(is_active=True).count(),
        'current_session': AcademicSession.objects.filter(is_current=True).first(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'pending_inquiries': AdmissionInquiry.objects.filter(status='pending').count(),
        'students_by_class': students_by_class,
        'max_count': max_count,
    }
    return render(request, 'accounts/dashboard_admin.html', context)


# ─── Teacher Dashboard ─────────────────────────────────────────────────────────

@teacher_required
def teacher_dashboard(request):
    """
    Teacher-only dashboard. Protected by @teacher_required.
    Admins can also access it since they supervise teachers.
    """
    user = request.user
    profile = _get_profile(user)

    teacher = None
    try:
        teacher = Teacher.objects.get(user=user)
    except Teacher.DoesNotExist:
        messages.warning(request, 'Your teacher profile is not yet linked. Please contact the administrator.')

    context = {
        'profile': profile,
        'role': 'teacher',
        'teacher': teacher,
        'subjects': teacher.subjects.filter(is_active=True) if teacher else [],
    }
    return render(request, 'accounts/dashboard_teacher.html', context)


# ─── Student Dashboard ─────────────────────────────────────────────────────────

@login_required(login_url='/accounts/login/')
def student_dashboard(request):
    """
    Student-only dashboard. An extra role check ensures non-students
    cannot access this URL directly.
    """
    user = request.user
    profile = _get_profile(user)

    # Block non-students from accessing this URL directly
    if not _is_student(user, profile):
        messages.error(request, 'Access denied. This dashboard is for students only.')
        return redirect('accounts:my_dashboard')

    student = None
    results = []
    try:
        student = Student.objects.get(user=user)
        current_session = AcademicSession.objects.filter(is_current=True).first()
        if current_session:
            results = Result.objects.filter(
                student=student, session=current_session
            ).select_related('subject')
    except Student.DoesNotExist:
        messages.warning(request, 'Your student profile is not yet linked. Please contact the administrator.')

    context = {
        'profile': profile,
        'role': 'student',
        'student': student,
        'results': results,
    }
    return render(request, 'accounts/dashboard_student.html', context)

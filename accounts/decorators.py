from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def _get_profile(user):
    from .models import UserProfile
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile


def admin_required(view_func):
    """
    Allows access only to superusers, staff users, or users with
    the 'admin' role in their UserProfile. All others are shown
    an 'Access Denied' message and redirected to their own dashboard
    (or to login if unauthenticated).
    """
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')

        user = request.user
        profile = _get_profile(user)

        if user.is_superuser or user.is_staff or profile.role == 'admin':
            return view_func(request, *args, **kwargs)

        # Non-admin users are blocked
        messages.error(
            request,
            'Access denied. You do not have permission to view the Admin Dashboard.'
        )
        # Redirect them to their own appropriate dashboard
        return redirect('accounts:my_dashboard')

    return _wrapped


def teacher_required(view_func):
    """Allows access only to teachers (and admins)."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')

        user = request.user
        profile = _get_profile(user)

        if user.is_superuser or user.is_staff or profile.role in ('admin', 'teacher'):
            return view_func(request, *args, **kwargs)

        messages.error(request, 'Access denied. This area is for teachers only.')
        return redirect('accounts:my_dashboard')

    return _wrapped

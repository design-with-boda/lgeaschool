from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages


@login_required(login_url='/accounts/login/')
def admin_dashboard_view(request):
    """
    Legacy entry-point kept for backward compatibility.
    All dashboard logic lives in accounts/views.py dashboard().
    """
    return redirect('accounts:dashboard')


def admin_login_view(request):
    """Redirect legacy /login/ to the main accounts login."""
    return redirect('accounts:login')


def admin_logout_view(request):
    """Redirect legacy /logout/ to the main accounts logout."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('accounts:login')

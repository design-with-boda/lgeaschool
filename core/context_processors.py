from .models import SchoolInfo, Announcement, SchoolEvent
from django.utils import timezone


def school_info(request):
    """Make school info available in all templates."""
    info = SchoolInfo.get_info()
    announcements = Announcement.objects.filter(is_active=True)[:5]
    upcoming_events = SchoolEvent.objects.filter(
        is_active=True,
        start_date__gte=timezone.now().date()
    )[:3]
    return {
        'school_info': info,
        'announcements': announcements,
        'upcoming_events': upcoming_events,
    }

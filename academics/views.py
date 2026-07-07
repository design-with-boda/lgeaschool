from django.shortcuts import render
from .models import Subject, AcademicSession, LearningMaterial


def academics_overview(request):
    sessions = AcademicSession.objects.all()
    current_session = sessions.filter(is_current=True).first()
    subjects_by_class = {}
    for cls in ['Nursery 1', 'Nursery 2', 'Primary 1', 'Primary 2', 'Primary 3',
                'Primary 4', 'Primary 5', 'Primary 6']:
        subjects_by_class[cls] = Subject.objects.filter(class_level=cls, is_active=True)
    return render(request, 'academics/overview.html', {
        'sessions': sessions,
        'current_session': current_session,
        'subjects_by_class': subjects_by_class,
    })


def materials_list(request):
    materials = LearningMaterial.objects.filter(is_public=True).select_related('subject', 'uploaded_by')
    class_filter = request.GET.get('class', '')
    if class_filter:
        materials = materials.filter(subject__class_level=class_filter)
    return render(request, 'academics/materials.html', {'materials': materials, 'class_filter': class_filter})

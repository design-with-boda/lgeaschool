from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Student, Attendance
from academics.models import Result, AcademicSession


def student_list(request):
    class_filter = request.GET.get('class', '')
    students = Student.objects.filter(is_active=True)
    if class_filter:
        students = students.filter(current_class=class_filter)
    return render(request, 'students/student_list.html', {'students': students, 'class_filter': class_filter})


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    current_session = AcademicSession.objects.filter(is_current=True).first()
    results = []
    if current_session:
        results = Result.objects.filter(student=student, session=current_session).select_related('subject')
    attendance = student.attendances.all()[:20]
    return render(request, 'students/student_detail.html', {
        'student': student,
        'results': results,
        'attendance': attendance,
        'current_session': current_session,
    })


@login_required
def result_check(request):
    student = None
    results = []
    session = None
    student_id = request.GET.get('student_id', '')
    session_id = request.GET.get('session', '')
    sessions = AcademicSession.objects.all()

    if student_id:
        try:
            student = Student.objects.get(student_id=student_id)
            if session_id:
                session = AcademicSession.objects.get(pk=session_id)
            else:
                session = AcademicSession.objects.filter(is_current=True).first()
            if session:
                results = Result.objects.filter(
                    student=student, session=session
                ).select_related('subject').order_by('subject__name')
        except (Student.DoesNotExist, AcademicSession.DoesNotExist):
            pass

    return render(request, 'students/result_check.html', {
        'student': student,
        'results': results,
        'session': session,
        'sessions': sessions,
        'student_id': student_id,
    })

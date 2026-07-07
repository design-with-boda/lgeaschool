from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_portal, name='login'),
    path('login/<str:role>/', views.login_role, name='login_role'),
    path('logout/', views.logout_view, name='logout'),

    # Role-specific dashboards — protected individually
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),

    # Generic dispatcher — redirects each user to their own dashboard
    path('dashboard/', views.my_dashboard, name='my_dashboard'),
    # Keep old name 'dashboard' as alias so existing {% url 'accounts:dashboard' %} still works
    path('me/', views.my_dashboard, name='dashboard'),
]


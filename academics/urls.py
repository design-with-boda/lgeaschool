from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    path('', views.academics_overview, name='overview'),
    path('materials/', views.materials_list, name='materials'),
]

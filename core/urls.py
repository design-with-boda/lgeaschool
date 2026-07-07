from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('admission/', views.admission, name='admission'),
    path('administration/', views.administration, name='administration'),
    path('documents/', views.documents, name='documents'),
    path('events/', views.events, name='events'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('templates/', views.templates, name='templates'),
    path('log/<int:template_id>/', views.log_workout, name='log_workout'),
    path('history/', views.history, name='history'),
]

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from workouts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('templates/', views.templates, name='templates'),
    path('templates/create/', views.create_template, name='create_template'),
    path('log/<int:template_id>/', views.log_workout, name='log_workout'),
    path('history/', views.history, name='history'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='workouts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),  # Add registration page
    path('templates/create/', views.create_template, name='create_template'),

]

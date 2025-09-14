from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "workouts/home.html")

@login_required(login_url='login')
def templates(request):
    # Example: return list of workout templates
    workout_templates = [
        {'id': 1, 'name': 'Full Body Workout'},
        {'id': 2, 'name': 'Upper Body Blast'},
    ]
    return render(request, "workouts/templates.html", {'templates': workout_templates})

@login_required(login_url='login')
def log_workout(request, template_id):
    # Here you can handle form submission for logging workout
    return render(request, "workouts/log_workout.html", {'template_id': template_id})

@login_required(login_url='login')
def history(request):
    # Example history data
    workout_history = [
        {'date': '2025-09-14', 'template': 'Full Body Workout'},
        {'date': '2025-09-13', 'template': 'Upper Body Blast'},
    ]
    return render(request, "workouts/history.html", {'history': workout_history})

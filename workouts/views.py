from django.shortcuts import render, redirect, get_object_or_404
from .models import WorkoutTemplate, TemplateExercise, Exercise, LoggedWorkout, LoggedExercise
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "workouts/home.html")

@login_required
def templates(request):
    user_templates = WorkoutTemplate.objects.filter(user=request.user)
    return render(request, "workouts/templates.html", {"templates": user_templates})

@login_required
def log_workout(request, template_id):
    template = get_object_or_404(WorkoutTemplate, id=template_id, user=request.user)
    if request.method == "POST":
        workout = LoggedWorkout.objects.create(user=request.user, template=template)
        for te in template.exercises.all():
            weight = request.POST.get(f"weight_{te.id}")
            reps = request.POST.get(f"reps_{te.id}")
            LoggedExercise.objects.create(
                workout=workout,
                exercise=te.exercise,
                weight=weight,
                reps=reps
            )
        return redirect("history")
    return render(request, "workouts/log_workout.html", {"template": template})

@login_required
def history(request):
    workouts = LoggedWorkout.objects.filter(user=request.user).order_by("-date")
    return render(request, "workouts/history.html", {"workouts": workouts})

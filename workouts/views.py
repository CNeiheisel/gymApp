from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import WorkoutTemplate, WorkoutEntry, Workout

# Home page
def home(request):
    return render(request, "workouts/home.html")

# User registration
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "workouts/register.html", {"form": form})

# Login page
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get("next", "home")
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, "workouts/login.html", {"form": form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect("home")

# List all workout templates
@login_required
def templates(request):
    templates = WorkoutTemplate.objects.all()
    return render(request, "workouts/templates.html", {"templates": templates})

# Log a workout based on a template
@login_required
def log_workout(request, template_id):
    template = get_object_or_404(WorkoutTemplate, id=template_id)
    
    if request.method == "POST":
        workout = Workout.objects.create(user=request.user, template=template)
        for te in template.exercises.all():
            weight = request.POST.get(f"weight_{te.id}")
            reps = request.POST.get(f"reps_{te.id}")
            if weight and reps:
                WorkoutEntry.objects.create(
                    workout=workout,
                    exercise=te.exercise,
                    weight=weight,
                    reps=reps
                )
        return redirect("history")

    return render(request, "workouts/log_workout.html", {"template": template})

# Show user's workout history
@login_required
def history(request):
    workouts = Workout.objects.filter(user=request.user).order_by("-date")
    return render(request, "workouts/history.html", {"workouts": workouts})

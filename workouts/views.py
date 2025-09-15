from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.http import require_POST
from django.forms import modelformset_factory
from .models import WorkoutTemplate, TemplateExercise, LoggedWorkout, LoggedExercise, Exercise
from .forms import WorkoutTemplateForm, TemplateExerciseForm

# ----------------------
# Home page
# ----------------------
def home(request):
    return render(request, "workouts/home.html")


# ----------------------
# User registration
# ----------------------
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("home")  # Redirect to home after registration
    else:
        form = UserCreationForm()
    return render(request, "workouts/register.html", {"form": form})


# ----------------------
# User login
# ----------------------
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get("next", "home")  # Redirect to 'next' or home
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, "workouts/login.html", {"form": form})


# ----------------------
# User logout (POST only)
# ----------------------
@require_POST
@login_required
def logout_view(request):
    logout(request)
    return redirect("home")


# ----------------------
# List all workout templates
# ----------------------
@login_required
def templates(request):
    templates = WorkoutTemplate.objects.filter(user=request.user)
    return render(request, "workouts/templates.html", {"templates": templates})


# ----------------------
# Create a new workout template with exercises
# ----------------------
@login_required
def create_template(request):
    ExerciseFormSet = modelformset_factory(
        TemplateExercise,
        form=TemplateExerciseForm,
        extra=1,
        can_delete=True
    )

    if request.method == "POST":
        template_form = WorkoutTemplateForm(request.POST)
        formset = ExerciseFormSet(request.POST, queryset=TemplateExercise.objects.none())

        if template_form.is_valid() and formset.is_valid():
            # Save template
            template = template_form.save(commit=False)
            template.user = request.user
            template.save()

            # Save exercises
            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    exercise = form.cleaned_data.get('exercise')
                    new_name = form.cleaned_data.get('new_exercise_name')
                    new_muscle = form.cleaned_data.get('new_muscle_group')

                    # Create new exercise if user entered a new one
                    if new_name:
                        exercise, created = Exercise.objects.get_or_create(
                            name=new_name,
                            defaults={'muscle_group': new_muscle or 'Unknown'}
                        )

                    template_exercise = TemplateExercise(
                        template=template,
                        exercise=exercise,
                        sets=form.cleaned_data.get('sets'),
                        reps=form.cleaned_data.get('reps')
                    )
                    template_exercise.save()

            return redirect('templates')

    else:
        template_form = WorkoutTemplateForm()
        formset = ExerciseFormSet(queryset=TemplateExercise.objects.none())

    return render(request, 'workouts/create_template.html', {
        'template_form': template_form,
        'formset': formset
    })


# ----------------------
# Log a workout based on a template
# ----------------------
@login_required
def log_workout(request, template_id):
    template = get_object_or_404(WorkoutTemplate, id=template_id, user=request.user)

    if request.method == "POST":
        workout = LoggedWorkout.objects.create(user=request.user, template=template)

        for te in template.exercises.all():  # TemplateExercise objects
            weight = request.POST.get(f"weight_{te.id}", 0)
            reps = request.POST.get(f"reps_{te.id}", te.reps)
            LoggedExercise.objects.create(
                workout=workout,
                exercise=te.exercise,
                weight=weight,
                reps=reps
            )

        return redirect("history")

    return render(request, "workouts/log_workout.html", {"template": template})
    
@login_required
def delete_template(request, template_id):
    template = get_object_or_404(WorkoutTemplate, id=template_id, user=request.user)
    if request.method == "POST":
        template.delete()
        messages.success(request, "Template deleted successfully.")
        return redirect('templates')
    return render(request, 'workouts/confirm_delete.html', {'template': template})


# ----------------------
# Show user's workout history
# ----------------------
@login_required
def history(request):
    workouts = LoggedWorkout.objects.filter(user=request.user).order_by("-date")
    return render(request, "workouts/history.html", {"workouts": workouts})

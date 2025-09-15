from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.forms import modelformset_factory
from django.contrib import messages
from .models import WorkoutTemplate, TemplateExercise, LoggedWorkout, LoggedExercise, Exercise
from .forms import WorkoutTemplateForm, TemplateExerciseForm

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

# List all workout templates
@login_required
def templates(request):
    templates = WorkoutTemplate.objects.filter(user=request.user)
    return render(request, "workouts/templates.html", {"templates": templates})

# Create a new workout template
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
            template = template_form.save(commit=False)
            template.user = request.user
            template.save()

            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    exercise = form.save(commit=False)
                    exercise.template = template
                    exercise.save()

            return redirect('templates')
    else:
        template_form = WorkoutTemplateForm()
        formset = ExerciseFormSet(queryset=TemplateExercise.objects.none())

    return render(request, 'workouts/create_template.html', {
        'template_form': template_form,
        'formset': formset
    })

# Edit an existing template (add/remove exercises)
@login_required
def edit_template(request, template_id):
    template = get_object_or_404(WorkoutTemplate, id=template_id, user=request.user)
    ExerciseFormSet = modelformset_factory(
        TemplateExercise,
        form=TemplateExerciseForm,
        extra=1,
        can_delete=True
    )

    if request.method == "POST":
        formset = ExerciseFormSet(request.POST, queryset=template.exercises.all())
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data.get('DELETE'):
                    if form.instance.id:
                        form.instance.delete()
                elif form.cleaned_data:
                    # Handle new exercise creation
                    new_ex_name =

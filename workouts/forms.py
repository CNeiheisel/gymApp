from django import forms
from .models import WorkoutTemplate, TemplateExercise, Exercise

class WorkoutTemplateForm(forms.ModelForm):
    class Meta:
        model = WorkoutTemplate
        fields = ['name']

class TemplateExerciseForm(forms.ModelForm):
    class Meta:
        model = TemplateExercise
        fields = ['exercise', 'sets', 'reps']


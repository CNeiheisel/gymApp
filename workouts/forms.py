from django import forms
from .models import WorkoutTemplate, TemplateExercise, Exercise

class WorkoutTemplateForm(forms.ModelForm):
    class Meta:
        model = WorkoutTemplate
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Template Name'}),
        }

class TemplateExerciseForm(forms.ModelForm):
    # New exercise fields
    new_exercise_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Exercise Name'})
    )
    new_muscle_group = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Muscle Group'})
    )

    class Meta:
        model = TemplateExercise
        fields = ['exercise', 'sets', 'reps']  # Optional: add 'weight'
        widgets = {
            'exercise': forms.Select(attrs={'class': 'form-select'}),
            'sets': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'reps': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

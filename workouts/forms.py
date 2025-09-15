from django import forms
from .models import WorkoutTemplate, TemplateExercise, Exercise

# Form for creating a workout template
class WorkoutTemplateForm(forms.ModelForm):
    class Meta:
        model = WorkoutTemplate
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Template Name'}),
        }

# Form for adding exercises to a template
class TemplateExerciseForm(forms.ModelForm):
    class Meta:
        model = TemplateExercise
        fields = ['exercise', 'sets', 'reps']  # Add 'weight' here if needed
        widgets = {
            'exercise': forms.Select(attrs={'class': 'form-select'}),
            'sets': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'reps': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            # 'weight': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.5}),
        }

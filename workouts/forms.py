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
    exercise = forms.ModelChoiceField(
        queryset=None,  # We'll set this in __init__
        required=False  # Make it optional
    )

    class Meta:
        model = TemplateExercise
        fields = ['exercise', 'sets', 'reps']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Exercise
        self.fields['exercise'].queryset = Exercise.objects.all()

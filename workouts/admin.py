from django.contrib import admin
from .models import Exercise, WorkoutTemplate, TemplateExercise, LoggedWorkout, LoggedExercise

admin.site.register(Exercise)
admin.site.register(WorkoutTemplate)
admin.site.register(TemplateExercise)
admin.site.register(LoggedWorkout)
admin.site.register(LoggedExercise)

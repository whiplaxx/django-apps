from django import forms

from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['description', 'dateLimit']
        labels = {
            'dateLimit': "Date limit"
        }

class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['description', 'dateLimit', 'concluded']
        labels = {
            'dateLimit': "Date limit",
            'concluded': "Concluded?"
        }


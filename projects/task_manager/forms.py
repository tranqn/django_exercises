"""ModelForms for the task manager."""
from django import forms
from .models import Project, Task


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name"]


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["project", "title", "notes", "status", "due_date"]
        widgets = {"due_date": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            # Only let users attach tasks to their own projects.
            self.fields["project"].queryset = Project.objects.filter(owner=user)
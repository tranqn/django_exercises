"""Task manager domain models."""
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Project(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name="projects")
    name = models.CharField(max_length=120)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    class Status(models.TextChoices):
        TODO = "todo", "To do"
        DOING = "doing", "In progress"
        DONE = "done", "Done"

    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                related_name="tasks")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name="tasks")
    title = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=Status.choices,
                              default=Status.TODO)
    due_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["due_date", "-created"]

    def get_absolute_url(self):
        return reverse("tasks:detail", args=[self.pk])

    @property
    def is_overdue(self):
        return (self.due_date and self.status != self.Status.DONE
                and self.due_date < timezone.localdate())

    def __str__(self):
        return self.title
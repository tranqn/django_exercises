"""Class-based CRUD views for tasks."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)

from .models import Task
from .forms import TaskForm
from .mixins import OwnerQuerysetMixin


class TaskListView(LoginRequiredMixin, OwnerQuerysetMixin, ListView):
    model = Task
    paginate_by = 20
    template_name = "tasks/task_list.html"


class TaskDetailView(LoginRequiredMixin, OwnerQuerysetMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:list")

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw["user"] = self.request.user
        return kw

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, OwnerQuerysetMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:list")

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw["user"] = self.request.user
        return kw

    def form_valid(self, form):
        if form.instance.status == Task.Status.DONE and not form.instance.completed_at:
            form.instance.completed_at = timezone.now()
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, OwnerQuerysetMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:list")
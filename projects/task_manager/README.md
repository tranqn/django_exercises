# Task Manager — Server-rendered Django

A multi-user task tracker built with class-based views, ModelForms and
templates. Each user sees only their own projects and tasks.

## Features
- Projects contain Tasks (todo / in-progress / done)
- Full CRUD with generic class-based views
- Owner-scoped querysets (users see only their own data)
- Dashboard with per-status counts
- Overdue-task management command

## Layout
    models.py     Project, Task
    forms.py      ProjectForm, TaskForm
    views.py      CBV CRUD
    mixins.py     OwnerQuerysetMixin
    urls.py       routes
    templates/    task_list.html, task_detail.html
# Task Manager — Setup & Usage

## Install
    INSTALLED_APPS += ["projects.task_manager"]
    path("tasks/", include("projects.task_manager.urls"))

## Migrate
    manage.py makemigrations task_manager
    manage.py migrate

## Daily ops
    manage.py overdue_tasks            # list overdue tasks
    manage.py overdue_tasks --notify   # email owners

## Ownership model
Every Project and Task has an owner. Views use OwnerQuerysetMixin, so a user
can only list, view, edit or delete their own rows — requesting another
user's task pk returns 404, not 403 (we don't reveal existence).

## Exercises
1. Add a "complete" button that PATCHes status to done via a small view.
2. Add tags to tasks with a ManyToManyField and filter the list by tag.
3. Add a calendar view grouping tasks by due_date (TruncDate).
4. Send a daily digest email of today's tasks with a Celery beat job.
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render


@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")


@permission_required("polls.add_question", raise_exception=True)
def create_question_view(request):
    """Only users with 'polls.add_question' permission can access."""
    return render(request, "accounts/create_question.html")


@permission_required("polls.change_question", raise_exception=True)
def edit_question_view(request):
    return render(request, "accounts/edit_question.html")
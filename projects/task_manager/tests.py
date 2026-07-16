"""Tests for the task manager."""
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Project, Task

pytestmark = pytest.mark.django_db
User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user("u", password="pw")


def test_completed_at_set_on_done(user):
    p = Project.objects.create(owner=user, name="P")
    t = Task.objects.create(owner=user, project=p, title="x", status="done")
    assert t.completed_at is not None


def test_user_cannot_see_others_task(client, user):
    other = User.objects.create_user("other", password="pw")
    p = Project.objects.create(owner=other, name="P")
    t = Task.objects.create(owner=other, project=p, title="secret")
    client.force_login(user)
    resp = client.get(reverse("tasks:detail", args=[t.pk]))
    assert resp.status_code == 404
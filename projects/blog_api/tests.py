"""API tests for the blog."""
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Post

pytestmark = pytest.mark.django_db
User = get_user_model()


@pytest.fixture
def author(db):
    return User.objects.create_user("author", password="pw")


@pytest.fixture
def author_client(author):
    c = APIClient()
    c.force_authenticate(author)
    return c


def test_anonymous_sees_only_published(author):
    Post.objects.create(title="Draft", author=author, body="x", status="draft")
    Post.objects.create(title="Live", author=author, body="x", status="published")
    resp = APIClient().get("/api/posts/")
    assert resp.status_code == 200
    assert [p["title"] for p in resp.json()["results"]] == ["Live"]


def test_author_can_create_post(author_client):
    resp = author_client.post("/api/posts/", {"title": "Hello", "body": "World"},
                              format="json")
    assert resp.status_code == 201
    assert resp.json()["slug"] == "hello"


def test_non_author_cannot_edit(author):
    post = Post.objects.create(title="Mine", author=author, body="x")
    intruder = User.objects.create_user("intruder", password="pw")
    c = APIClient()
    c.force_authenticate(intruder)
    resp = c.patch(f"/api/posts/{post.slug}/", {"title": "Hacked"}, format="json")
    assert resp.status_code == 403
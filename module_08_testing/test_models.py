import pytest
from django.utils import timezone

pytestmark = pytest.mark.django_db


def test_user_str_returns_username(user):
    assert str(user) == "tester"


def test_user_email_is_stored(django_user_model):
    u = django_user_model.objects.create_user(
        username="alice", email="alice@example.com", password="x"
    )
    assert u.email == "alice@example.com"


def test_create_user_requires_username(django_user_model):
    with pytest.raises(TypeError):
        django_user_model.objects.create_user(email="a@b.com", password="x")


def test_date_joined_is_set(user):
    assert user.date_joined <= timezone.now()
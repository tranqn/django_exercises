"""Shared pytest fixtures for the test suite.

Run the suite:
    pytest
    pytest -k "model and not slow"
    pytest --cov=. --cov-report=term-missing
"""
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="tester", email="tester@example.com", password="pass1234"
    )


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client
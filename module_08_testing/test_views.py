import pytest

pytestmark = pytest.mark.django_db


def test_home_view_ok(client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_login_required_redirects(client):
    resp = client.get("/dashboard/")
    assert resp.status_code == 302
    assert "/login" in resp.url


def test_login_then_access_dashboard(client, user):
    client.force_login(user)
    resp = client.get("/dashboard/")
    assert resp.status_code == 200
    assert b"tester" in resp.content
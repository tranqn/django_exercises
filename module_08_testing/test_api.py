import pytest

pytestmark = pytest.mark.django_db


def test_unauthenticated_request_is_rejected(api_client):
    resp = api_client.get("/api/books/")
    assert resp.status_code in (401, 403)


def test_authenticated_list_returns_200(auth_client):
    resp = auth_client.get("/api/books/")
    assert resp.status_code == 200


def test_create_book(auth_client):
    payload = {"title": "Django Unleashed", "pages": 420}
    resp = auth_client.post("/api/books/", payload, format="json")
    assert resp.status_code == 201
    assert resp.json()["title"] == "Django Unleashed"


@pytest.mark.parametrize("page,expected", [(1, 200), (999, 404)])
def test_pagination_bounds(auth_client, page, expected):
    resp = auth_client.get(f"/api/books/?page={page}")
    assert resp.status_code == expected
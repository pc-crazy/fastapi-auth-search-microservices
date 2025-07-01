import pytest
from fastapi.testclient import TestClient
from services.search_service.main import app
from services.search_service.tests.utils import (
    create_test_token,
    create_expired_token,
    create_invalid_token,
)
from unittest.mock import patch

client = TestClient(app)


@pytest.fixture
def auth_header():
    token = create_test_token(user_id=1, org_id=1)
    return {"Authorization": f"Bearer {token}"}


# ✅ Automatically bypass rate limiting in all tests unless testing 429
@pytest.fixture(autouse=True)
def bypass_rate_limit():
    with patch("services.search_service.main.is_allowed", return_value=True):
        yield


# ✅ Auth tests
def test_missing_authorization():
    response = client.get("/search")
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"


def test_malformed_authorization():
    headers = {"Authorization": "TokenXYZ"}
    response = client.get("/search", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"


def test_expired_token():
    token = create_expired_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/search", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Token expired"


def test_invalid_signature():
    token = create_invalid_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/search", headers=headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid token"


# ✅ General response structure
def test_search_structure(auth_header):
    response = client.get("/search", headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "count" in data
    assert "next" in data
    assert "previous" in data
    assert "results" in data
    assert isinstance(data["results"], list)


# ✅ Pagination test
def test_search_pagination(auth_header):
    response = client.get("/search?limit=5&offset=0", headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert data["count"] <= 5
    assert data["total"] >= data["count"]


# ✅ All expected fields test
def test_all_columns_returned(auth_header):
    response = client.get("/search", headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    if data["results"]:
        item = data["results"][0]
        for col in [
            "first_name",
            "last_name",
            "status",
            "location",
            "company",
            "department",
            "position",
        ]:
            assert col in item


# ✅ Individual filter tests
def test_filter_by_status(auth_header):
    response = client.get("/search?status=1", headers=auth_header)
    assert response.status_code == 200
    for emp in response.json()["results"]:
        assert emp["status"] == "active"


def test_filter_by_location(auth_header):
    response = client.get("/search?location=Delhi", headers=auth_header)
    assert response.status_code == 200
    for emp in response.json()["results"]:
        assert "Delhi" in emp["location"]


def test_filter_by_company(auth_header):
    response = client.get("/search?company=Google", headers=auth_header)
    assert response.status_code == 200
    for emp in response.json()["results"]:
        assert "Google" in emp["company"]


def test_filter_by_department(auth_header):
    response = client.get("/search?department=Engineering", headers=auth_header)
    assert response.status_code == 200
    for emp in response.json()["results"]:
        assert "Engineering" in emp["department"]


def test_filter_by_position(auth_header):
    response = client.get("/search?position=Developer", headers=auth_header)
    assert response.status_code == 200
    for emp in response.json()["results"]:
        assert "Developer" in emp["position"]


# ✅ Combined filters and pagination
def test_combined_filter_and_pagination(auth_header):
    response = client.get(
        "/search?status=1&location=Delhi&limit=5", headers=auth_header
    )
    assert response.status_code == 200
    data = response.json()
    assert data["count"] <= 5
    for emp in data["results"]:
        assert emp["status"] == "active"
        assert "Delhi" in emp["location"]


# ✅ q= search test
def test_search_with_query(auth_header):
    response = client.get("/search?q=Google", headers=auth_header)
    assert response.status_code == 200
    for emp in response.json()["results"]:
        assert "Google" in emp["company"] or "Google" in emp["first_name"] or "Google" in emp["last_name"]


# ✅ Test for rate limit rejection (429)
def test_rate_limit_exceeded_response():
    with patch("services.search_service.main.is_allowed", return_value=False):
        token = create_test_token(user_id=1, org_id=1)
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/search", headers=headers)
        assert response.status_code == 429
        assert response.json() == {"detail": "Rate limit exceeded"}

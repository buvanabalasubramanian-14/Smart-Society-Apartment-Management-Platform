import sys
from pathlib import Path

backend_path = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(backend_path))

from app import app


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_home():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200


def test_login_page():
    client = app.test_client()

    response = client.get("/login")

    assert response.status_code == 200


def test_register_page():
    client = app.test_client()

    response = client.get("/register")

    assert response.status_code == 200


def test_admin_login_page():
    client = app.test_client()

    response = client.get("/admin/login")

    assert response.status_code == 200


def test_dashboard_requires_login():
    client = app.test_client()

    response = client.get("/dashboard")

    assert response.status_code == 302


def test_admin_dashboard_requires_login():
    client = app.test_client()

    response = client.get("/admin/dashboard")

    assert response.status_code == 302


def test_complaints_requires_login():
    client = app.test_client()

    response = client.get("/complaints")

    assert response.status_code == 302


def test_maintenance_requires_login():
    client = app.test_client()

    response = client.get("/maintenance")

    assert response.status_code == 302


def test_visitors_requires_login():
    client = app.test_client()

    response = client.get("/visitors")

    assert response.status_code == 302
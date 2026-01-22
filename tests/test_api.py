import uuid
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def random_email() -> str:
    return f"test_{uuid.uuid4().hex[:8]}@example.com"


def signup_and_login():
    email = random_email()
    password = "test1234"

    # signup
    r = client.post("/signup", json={"name": "Test User", "email": email, "password": password})
    assert r.status_code in (200, 409)

    # login-json (easy for tests)
    r = client.post("/login-json", json={"email": email, "password": password})
    assert r.status_code == 200
    token = r.json()["access_token"]

    return token, email


def test_protected_create_class_requires_auth():
    r = client.post(
        "/classes",
        json={
            "name": "Yoga Flow",
            "dateTime": "2026-02-10T10:00:00Z",
            "instructor": "John Doe",
            "availableSlots": 5,
        },
    )
    assert r.status_code == 401


def test_create_class_and_booking_flow():
    token, email = signup_and_login()
    headers = {"Authorization": f"Bearer {token}"}

    # create class with 2 slots
    r = client.post(
        "/classes",
        headers=headers,
        json={
            "name": "HIIT Session",
            "dateTime": "2026-02-10T10:00:00Z",
            "instructor": "Coach",
            "availableSlots": 2,
        },
    )
    assert r.status_code == 200
    class_id = r.json()["id"]

    # book once -> slots should reduce to 1
    r = client.post(
        "/book",
        headers=headers,
        json={
            "class_id": class_id,
            "client_name": "Test User",
            "client_email": email,
        },
    )
    assert r.status_code == 200
    assert r.json()["remaining_slots"] == 1

    # duplicate booking should fail
    r = client.post(
        "/book",
        headers=headers,
        json={
            "class_id": class_id,
            "client_name": "Test User",
            "client_email": email,
        },
    )
    assert r.status_code == 409

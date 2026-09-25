import os

os.environ["SECRET_KEY"] = "test-secret"

os.environ["DATABASE_URL"] = (
    "sqlite:///./test_pocketsmart.db"
)

os.environ["GEMINI_API_KEY"] = ""


from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert (
        response.json()["status"]
        == "ok"
    )


def test_register_rejects_password_longer_than_bcrypt_limit():

    long_password = "a" * 73

    response = client.post(
        "/api/register",
        json={
            "name": "Tester",
            "email": "longpass@example.com",
            "password": long_password,
        },
    )

    assert response.status_code == 422


def test_register_login_and_home():

    email = (
        "tester@example.com"
    )


    response = client.post(
        "/api/register",
        json={
            "name": "Tester",
            "email": email,
            "password": "secret123",
        },
    )


    if response.status_code == 409:

        response = client.post(
            "/api/login",
            json={
                "email": email,
                "password": "secret123",
            },
        )


    assert response.status_code == 200


    token = response.json()["access_token"]


    response = client.post(

        "/api/generate-home",

        headers={
            "Authorization":
                f"Bearer {token}"
        },

        json={
            "budget": 50000,

            "rooms": [
                "Living Room"
            ],

            "style":
                "Modern",

            "requirements":
                "Storage",
        },
    )


    assert response.status_code == 200

    assert (
        response.json()["planner_type"]
        == "home"
    )

    assert len(
        response.json()[
            "recommendations"
        ]
    ) > 0
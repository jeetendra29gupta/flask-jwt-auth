import pytest

from main_app import app, db


@pytest.fixture(scope="module")
def test_client():
    # Create a test client
    with app.test_client() as client:
        # Establish an application context
        with app.app_context():
            # Create all tables
            db.create_all()
        yield client
        # Cleanup after tests
        with app.app_context():
            db.drop_all()


def test_signup(test_client):
    response = test_client.post(
        "/api/signup", json={"username": "test_user", "password": "password123"}
    )
    assert response.status_code == 201
    assert b"User created successfully" in response.data


def test_login(test_client):
    test_client.post(
        "/api/signup", json={"username": "test_user", "password": "password123"}
    )
    response = test_client.post(
        "/api/login", json={"username": "test_user", "password": "password123"}
    )
    assert response.status_code == 200
    assert b"Login successful" in response.data
    assert b"access_token" in response.data


def test_protected(test_client):
    # Create a user and get their access token
    response = test_client.post(
        "/api/signup", json={"username": "test_user", "password": "password123"}
    )
    response = test_client.post(
        "/api/login", json={"username": "test_user", "password": "password123"}
    )
    access_token = response.json["access_token"]

    # Use the access token to access the protected route
    response = test_client.get(
        "/api/protected", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert b"logged_in_as" in response.data


def test_logout(test_client):
    # Create a user and login
    response = test_client.post(
        "/api/signup", json={"username": "test_user", "password": "password123"}
    )
    response = test_client.post(
        "/api/login", json={"username": "test_user", "password": "password123"}
    )
    access_token = response.json["access_token"]

    # Logout
    response = test_client.delete(
        "/api/logout", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert b"Successfully logged out" in response.data


if __name__ == "__main__":
    pytest.main()

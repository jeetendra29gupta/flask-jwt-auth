import requests

BASE_URL = "http://127.0.0.1:8181"


def signup(username, password):
    url = f"{BASE_URL}/api/signup"
    payload = {"username": username, "password": password}
    response = requests.post(url, json=payload)
    print("Signup Response:", response.json())
    return response


def login(username, password):
    url = f"{BASE_URL}/api/login"
    payload = {"username": username, "password": password}
    response = requests.post(url, json=payload)
    print("Login Response:", response.json()["message"])
    return response


def refresh(refresh_token):
    url = f"{BASE_URL}/api/refresh"
    headers = {"Authorization": f"Bearer {refresh_token}"}
    response = requests.post(url, headers=headers)
    print("Refresh Response:", response.json())
    return response


def protected(access_token):
    url = f"{BASE_URL}/api/protected"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    print("Protected Response:", response.json())
    return response


def logout(access_token):
    url = f"{BASE_URL}/api/logout"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.delete(url, headers=headers)
    print("Logout Response:", response.json())
    return response


if __name__ == "__main__":
    # Test the routes

    print("\n--- Testing Signup ---")
    signup_response = signup("test_user", "password123")

    print("\n--- Testing Login ---")
    login_response = login("test_user", "password123")

    if login_response.status_code == 200:

        access_token = login_response.json().get("access_token")
        refresh_token = login_response.json().get("refresh_token")

        print("\n--- Testing Protected Route with Access Token ---")
        protected_response = protected(access_token)

        print("\n--- Testing Token Refresh ---")
        refresh_response = refresh(refresh_token)

        if refresh_response.status_code == 200:
            new_access_token = refresh_response.json().get("access_token")
            print("\n--- Testing Protected Route with New Access Token ---")
            protected(new_access_token)

        print("\n--- Testing Logout ---")
        logout_response = logout(access_token)

        print("\n--- Testing Protected Route After Logout ---")
        protected(access_token)

import pytest
from fastapi.testclient import TestClient

def test_login_success(client: TestClient):
    # Test data
    user_data = {
        "email": "login_email@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    
    # Make request
    response = client.post("/users/signup", json=user_data)

    login_data = {
        "email": "login_email@example.com",
        "password": "testpassword123"
    }

    response = client.post("/login", json=login_data)
    
    # Assertions
    assert response.status_code == 200
    assert response.json()["message"] == "User logged in successfully"

def test_login_wrong_password(client: TestClient):
    # Create user
    user_data = {
        "email": "wrong_pass@example.com",
        "password": "correctpassword123",
        "full_name": "Test User"
    }
    response = client.post("/users/signup", json=user_data)
    assert response.status_code == 200

    # Try login with wrong password
    login_data = {
        "email": "wrong_pass@example.com",
        "password": "wrongpassword123"
    }
    response = client.post("/login", json=login_data)
    
    # Assertions
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid password"

def test_login_nonexistent_user(client: TestClient):
    # Try login with non-existent email
    login_data = {
        "email": "nonexistent@example.com",
        "password": "password123"
    }
    response = client.post("/login", json=login_data)
    
    # Assertions
    assert response.status_code == 400
    assert response.json()["detail"] == "User not found"

def test_login_invalid_email_format(client: TestClient):
    # Try login with invalid email format
    login_data = {
        "email": "not-an-email",
        "password": "password123"
    }
    response = client.post("/login", json=login_data)
    
    # Assertions
    assert response.status_code == 422
    assert "email" in response.json()["detail"][0]["loc"]

def test_login_short_password(client: TestClient):
    # Try login with too short password
    login_data = {
        "email": "test@example.com",
        "password": "short"
    }
    response = client.post("/login", json=login_data)
    
    # Assertions
    assert response.status_code == 422
    assert "password" in response.json()["detail"][0]["loc"]

# def test_protected_route_without_token(client: TestClient):
#     # Try to access protected route without token
#     response = client.get("/users/me")
    
#     # Assertions
#     assert response.status_code == 401
#     assert response.json()["detail"] == "Not authenticated"

# def test_protected_route_with_token(client: TestClient):
#     # Create and login user
#     user_data = {
#         "email": "protected@example.com",
#         "password": "testpassword123",
#         "full_name": "Protected User"
#     }
#     client.post("/users/signup", json=user_data)
    
#     login_response = client.post("/login", json={
#         "email": "protected@example.com",
#         "password": "testpassword123"
#     })
#     assert login_response.status_code == 200
    
#     # Get token
#     token = login_response.json()["access_token"]
    
#     # Access protected route with token
#     headers = {"Authorization": f"Bearer {token}"}
#     response = client.get("/users/me", headers=headers)
    
#     # Assertions
#     assert response.status_code == 200
#     assert response.json()["email"] == "protected@example.com"

# def test_protected_route_with_invalid_token(client: TestClient):
#     # Try to access protected route with invalid token
#     headers = {"Authorization": "Bearer invalid_token"}
#     response = client.get("/users/me", headers=headers)
    
#     # Assertions
#     assert response.status_code == 401
#     assert response.json()["detail"] == "Could not validate credentials"
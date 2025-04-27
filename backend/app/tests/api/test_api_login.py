import pytest
from fastapi.testclient import TestClient

# def test_login_success(client: TestClient):
#     # Test data
#     user_data = {
#         "email": "login_email@example.com",
#         "password": "testpassword123",
#         "full_name": "Test User"
#     }
    
#     # Make request
#     response = client.post("/users/signup", json=user_data)

#     login_data = {
#         "email": "login_email@example.com",
#         "password": "testpassword123"
#     }

#     response = client.post("/login", json=login_data)
    
#     # Assertions
#     assert response.status_code == 200
#     assert response.json()["message"] == "User logged in successfully"

# def test_login_wrong_password(client: TestClient):
#     # Create user
#     user_data = {
#         "email": "wrong_pass@example.com",
#         "password": "correctpassword123",
#         "full_name": "Test User"
#     }
#     response = client.post("/users/signup", json=user_data)
#     assert response.status_code == 200

#     # Try login with wrong password
#     login_data = {
#         "email": "wrong_pass@example.com",
#         "password": "wrongpassword123"
#     }
#     response = client.post("/login", json=login_data)
    
#     # Assertions
#     assert response.status_code == 400
#     assert response.json()["detail"] == "Invalid password"

# def test_login_nonexistent_user(client: TestClient):
#     # Try login with non-existent email
#     login_data = {
#         "email": "nonexistent@example.com",
#         "password": "password123"
#     }
#     response = client.post("/login", json=login_data)
    
#     # Assertions
#     assert response.status_code == 400
#     assert response.json()["detail"] == "User not found"

# def test_login_invalid_email_format(client: TestClient):
#     # Try login with invalid email format
#     login_data = {
#         "email": "not-an-email",
#         "password": "password123"
#     }
#     response = client.post("/login", json=login_data)
    
#     # Assertions
#     assert response.status_code == 422
#     assert "email" in response.json()["detail"][0]["loc"]

# def test_login_short_password(client: TestClient):
#     # Try login with too short password
#     login_data = {
#         "email": "test@example.com",
#         "password": "short"
#     }
#     response = client.post("/login", json=login_data)
    
#     # Assertions
#     assert response.status_code == 422
#     assert "password" in response.json()["detail"][0]["loc"]

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

def test_password_reset_request(client: TestClient):
    # Create test user first
    user_data = {
        "email": "reset_test3@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    response = client.post("/users/signup", json=user_data)
    assert response.status_code == 200

    # Request password reset
    reset_request = {
        "email": user_data["email"]
    }
    response = client.post("/login/password-reset", json=reset_request)
    assert response.status_code == 200
    assert response.json()["message"] == "Password reset email sent successfully"

def test_password_reset_request_nonexistent_user(client: TestClient):
    # Request password reset for non-existent user
    reset_request = {
        "email": "nonexisten2t@example.com"
    }
    response = client.post("/login/password-reset", json=reset_request)
    assert response.status_code == 400
    assert response.json()["detail"] == "User not found"

def test_password_reset_with_token(client: TestClient):
    # Create test user
    user_data = {
        "email": "reset_token_test3@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    response = client.post("/users/signup", json=user_data)
    assert response.status_code == 200

    # Get user and generate reset token
    from app.utils import generate_password_reset_token
    from app import crud
    from app.core.db import engine
    from sqlalchemy.orm import Session
    
    with Session(engine) as session:
        user = crud.get_user_by_email(session=session, email=user_data["email"])
        reset_token = generate_password_reset_token(str(user.id))
    
    # Reset password with token
    new_password_data = {
        "token": reset_token,
        "new_password": "newpassword123"
    }
    response = client.post("/login/reset-password", json=new_password_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Password updated successfully"
    
    # Try to login with new password
    login_data = {
        "email": user_data["email"],
        "password": "newpassword123"
    }
    response = client.post("/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_password_reset_invalid_token(client: TestClient):
    # Try to reset password with invalid token
    new_password_data = {
        "token": "invalid_token",
        "new_password": "newpassword123"
    }
    response = client.post("/login/reset-password", json=new_password_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid or expired token"


import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user_success():
    # Test data
    user_data = {
        "email": "abc1@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    
    # Make request
    response = client.post("/users/signup", json=user_data)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "user_id" in data
    assert data["message"] == "User created successfully"

def test_create_user_duplicate_email():
    # Create first user
    user_data = {
        "email": "dup1@example.com",
        "password": "password123",
        "full_name": "First User"
    }
    client.post("/users/signup", json=user_data)
    
    # Try to create second user with same email
    response = client.post("/users/signup", json=user_data)
    
    # Assertions
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_create_user_invalid_email():
    # Test data with invalid email
    user_data = {
        "email": "invalid-email",
        "password": "password123",
        "full_name": "Test User"
    }
    
    # Make request
    response = client.post("/users/signup", json=user_data)
    
    # Assertions
    assert response.status_code == 422  # Validation error
    assert "email" in response.json()["detail"][0]["loc"]

def test_create_user_short_password():
    # Test data with short password
    user_data = {
        "email": "test@example.com",
        "password": "short",  # Less than 8 characters
        "full_name": "Test User"
    }
    
    # Make request
    response = client.post("/users/signup", json=user_data)
    
    # Assertions
    assert response.status_code == 422  # Validation error
    assert "password" in response.json()["detail"][0]["loc"]

def test_create_user_without_fullname():
    # Test data without full_name
    user_data = {
        "email": "nofullname@example.com",
        "password": "testpassword123"
    }
    
    # Make request
    response = client.post("/users/signup", json=user_data)
    
    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "user_id" in data
    assert data["message"] == "User created successfully" 
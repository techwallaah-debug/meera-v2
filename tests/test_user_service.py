"""
Tests for User Service
"""
import pytest
from fastapi.testclient import TestClient


def test_register_user(client, test_user):
    """Test user registration"""
    response = client.post("/register", json=test_user)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["username"] == test_user["username"]
    assert "id" in data
    assert "hashed_password" not in data


def test_register_duplicate_email(client, test_user):
    """Test duplicate email registration"""
    client.post("/register", json=test_user)
    response = client.post("/register", json=test_user)
    assert response.status_code == 400


def test_login_success(client, test_user):
    """Test successful login"""
    client.post("/register", json=test_user)
    response = client.post(
        "/token",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client, test_user):
    """Test login with invalid credentials"""
    client.post("/register", json=test_user)
    response = client.post(
        "/token",
        data={
            "username": test_user["email"],
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401


def test_get_current_user(client, auth_token):
    """Test getting current user"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "email" in data


def test_get_current_user_unauthorized(client):
    """Test getting current user without token"""
    response = client.get("/users/me")
    assert response.status_code == 401


def test_update_profile(client, auth_token):
    """Test updating user profile"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    update_data = {
        "full_name": "Updated Name",
        "bio": "Updated bio"
    }
    response = client.put("/users/me", json=update_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"
    assert data["bio"] == "Updated bio"


def test_get_user_by_id(client, test_user, auth_token):
    """Test getting user by ID"""
    # First get current user to get ID
    headers = {"Authorization": f"Bearer {auth_token}"}
    current_user = client.get("/users/me", headers=headers).json()
    user_id = current_user["id"]
    
    # Get user by ID
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id

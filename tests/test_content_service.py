"""
Tests for Content Service
"""
import pytest
from fastapi.testclient import TestClient


def test_create_post(client, auth_token):
    """Test creating a post"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    post_data = {
        "caption": "Test post",
        "media_urls": ["https://example.com/image.jpg"],
        "product_tags": []
    }
    response = client.post("/posts", json=post_data, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["caption"] == "Test post"
    assert "id" in data


def test_get_feed(client, auth_token):
    """Test getting feed"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Create a post first
    post_data = {
        "caption": "Test post",
        "media_urls": [],
        "product_tags": []
    }
    client.post("/posts", json=post_data, headers=headers)
    
    # Get feed
    response = client.get("/posts", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_like_post(client, auth_token):
    """Test liking a post"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Create a post
    post_data = {
        "caption": "Test post",
        "media_urls": [],
        "product_tags": []
    }
    post = client.post("/posts", json=post_data, headers=headers).json()
    post_id = post["id"]
    
    # Like post
    response = client.post(f"/posts/{post_id}/like", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["liked"] == True
    assert data["like_count"] == 1


def test_create_comment(client, auth_token):
    """Test creating a comment"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Create a post
    post_data = {
        "caption": "Test post",
        "media_urls": [],
        "product_tags": []
    }
    post = client.post("/posts", json=post_data, headers=headers).json()
    post_id = post["id"]
    
    # Create comment
    comment_data = {"content": "Test comment"}
    response = client.post(
        f"/posts/{post_id}/comments",
        json=comment_data,
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["content"] == "Test comment"

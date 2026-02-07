"""
Tests for Product Service
"""
import pytest
from fastapi.testclient import TestClient


def test_create_product(client, auth_token):
    """Test creating a product"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    product_data = {
        "title": "Test Product",
        "description": "Test description",
        "category": "fashion",
        "price": 999.99,
        "image_urls": ["https://example.com/image.jpg"],
        "stock_quantity": 10,
        "sku": "TEST-001"
    }
    response = client.post("/products", json=product_data, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Product"
    assert data["price"] == 999.99


def test_get_product(client, auth_token):
    """Test getting a product"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Create product
    product_data = {
        "title": "Test Product",
        "category": "fashion",
        "price": 999.99,
        "image_urls": [],
        "stock_quantity": 10,
        "sku": "TEST-002"
    }
    product = client.post("/products", json=product_data, headers=headers).json()
    product_id = product["id"]
    
    # Get product
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id


def test_search_products(client):
    """Test searching products"""
    response = client.get("/products", params={"q": "test"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_create_review(client, auth_token):
    """Test creating a product review"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Create product
    product_data = {
        "title": "Test Product",
        "category": "fashion",
        "price": 999.99,
        "image_urls": [],
        "stock_quantity": 10,
        "sku": "TEST-003"
    }
    product = client.post("/products", json=product_data, headers=headers).json()
    product_id = product["id"]
    
    # Create review
    review_data = {
        "rating": 5,
        "title": "Great product",
        "content": "Very satisfied"
    }
    response = client.post(
        f"/products/{product_id}/reviews",
        json=review_data,
        headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["rating"] == 5

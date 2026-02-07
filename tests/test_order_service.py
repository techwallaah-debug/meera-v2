"""
Tests for Order Service
"""
import pytest
from fastapi.testclient import TestClient


def test_add_to_cart(client, auth_token):
    """Test adding item to cart"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    cart_data = {
        "product_id": 1,
        "quantity": 2
    }
    response = client.post("/cart", json=cart_data, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["product_id"] == 1
    assert data["quantity"] == 2


def test_get_cart(client, auth_token):
    """Test getting cart"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Add item to cart
    cart_data = {"product_id": 1, "quantity": 1}
    client.post("/cart", json=cart_data, headers=headers)
    
    # Get cart
    response = client.get("/cart", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_update_cart_item(client, auth_token):
    """Test updating cart item quantity"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Add item to cart
    cart_data = {"product_id": 1, "quantity": 1}
    cart_item = client.post("/cart", json=cart_data, headers=headers).json()
    item_id = cart_item["id"]
    
    # Update quantity
    response = client.put(
        f"/cart/{item_id}",
        params={"quantity": 3},
        headers=headers
    )
    assert response.status_code == 200


def test_remove_from_cart(client, auth_token):
    """Test removing item from cart"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Add item to cart
    cart_data = {"product_id": 1, "quantity": 1}
    cart_item = client.post("/cart", json=cart_data, headers=headers).json()
    item_id = cart_item["id"]
    
    # Remove item
    response = client.delete(f"/cart/{item_id}", headers=headers)
    assert response.status_code == 200


def test_create_order(client, auth_token):
    """Test creating an order"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Add item to cart first
    cart_data = {"product_id": 1, "quantity": 1}
    client.post("/cart", json=cart_data, headers=headers)
    
    # Create order
    order_data = {
        "address": {
            "name": "Test User",
            "phone": "1234567890",
            "street": "123 Test St",
            "city": "Test City",
            "state": "Test State",
            "pincode": "123456"
        },
        "payment_method": "cod"
    }
    response = client.post("/orders", json=order_data, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert "order_number" in data
    assert data["payment_method"] == "cod"


def test_get_orders(client, auth_token):
    """Test getting user orders"""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/orders", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

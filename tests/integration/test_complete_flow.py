"""
Integration tests for complete user flows
"""
import pytest
from fastapi.testclient import TestClient


def test_complete_shopping_flow(client, test_user):
    """Test complete shopping flow: Register -> Login -> Browse -> Cart -> Checkout"""
    # 1. Register
    register_response = client.post("/register", json=test_user)
    assert register_response.status_code == 201
    
    # 2. Login
    login_response = client.post(
        "/token",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Create a product (as seller)
    product_data = {
        "title": "Test Product",
        "category": "fashion",
        "price": 999.99,
        "image_urls": [],
        "stock_quantity": 10,
        "sku": "FLOW-001"
    }
    product_response = client.post("/products", json=product_data, headers=headers)
    assert product_response.status_code == 201
    product_id = product_response.json()["id"]
    
    # 4. Add to cart
    cart_response = client.post(
        "/cart",
        json={"product_id": product_id, "quantity": 1},
        headers=headers
    )
    assert cart_response.status_code == 201
    
    # 5. Get cart
    cart_get = client.get("/cart", headers=headers)
    assert cart_get.status_code == 200
    assert len(cart_get.json()) > 0
    
    # 6. Create order
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
    order_response = client.post("/orders", json=order_data, headers=headers)
    assert order_response.status_code == 201
    order = order_response.json()
    assert "order_number" in order
    
    # 7. Get order details
    order_id = order["id"]
    order_details = client.get(f"/orders/{order_id}", headers=headers)
    assert order_details.status_code == 200


def test_social_commerce_flow(client, test_user):
    """Test social commerce flow: Post -> Like -> Comment -> Product Tag"""
    # Login
    login_response = client.post(
        "/token",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create product
    product_data = {
        "title": "Social Product",
        "category": "fashion",
        "price": 499.99,
        "image_urls": [],
        "stock_quantity": 5,
        "sku": "SOCIAL-001"
    }
    product = client.post("/products", json=product_data, headers=headers).json()
    product_id = product["id"]
    
    # Create post with product tag
    post_data = {
        "caption": "Check out this amazing product!",
        "media_urls": ["https://example.com/image.jpg"],
        "product_tags": [product_id]
    }
    post_response = client.post("/posts", json=post_data, headers=headers)
    assert post_response.status_code == 201
    post_id = post_response.json()["id"]
    
    # Like post
    like_response = client.post(f"/posts/{post_id}/like", headers=headers)
    assert like_response.status_code == 200
    
    # Comment on post
    comment_data = {"content": "Looks great!"}
    comment_response = client.post(
        f"/posts/{post_id}/comments",
        json=comment_data,
        headers=headers
    )
    assert comment_response.status_code == 201

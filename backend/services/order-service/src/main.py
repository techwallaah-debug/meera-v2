"""
Order Service - Handles shopping cart, checkout, orders, and payments
Port: 8004
"""
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey, Enum as SQLEnum
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum
import os
import json
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from shared.database.connection import get_db, Base, engine
from shared.auth.jwt import verify_token
from fastapi.security import OAuth2PasswordBearer

# Razorpay integration
try:
    import razorpay
    razorpay_client = razorpay.Client(
        auth=(os.getenv('RAZORPAY_KEY_ID', ''), os.getenv('RAZORPAY_KEY_SECRET', ''))
    )
    RAZORPAY_ENABLED = True
except:
    RAZORPAY_ENABLED = False

app = FastAPI(
    title="Order Service",
    version="1.0.0",
    description="Shopping cart, checkout, orders, and payment processing"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Enums
class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    RETURNED = "returned"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class PaymentMethod(str, Enum):
    RAZORPAY = "razorpay"
    COD = "cod"

# Database Models
class Cart(Base):
    __tablename__ = "carts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    order_number = Column(String(50), unique=True, index=True, nullable=False)
    total_amount = Column(Float, nullable=False)
    shipping_amount = Column(Float, default=50.0)
    discount_amount = Column(Float, default=0.0)
    final_amount = Column(Float, nullable=False)
    
    # Address
    shipping_name = Column(String(255), nullable=False)
    shipping_phone = Column(String(20), nullable=False)
    shipping_street = Column(Text, nullable=False)
    shipping_city = Column(String(100), nullable=False)
    shipping_state = Column(String(100), nullable=False)
    shipping_pincode = Column(String(10), nullable=False)
    
    # Payment
    payment_method = Column(String(50), nullable=False)
    payment_status = Column(String(50), default=PaymentStatus.PENDING.value)
    payment_id = Column(String(255), nullable=True)  # Razorpay payment ID
    razorpay_order_id = Column(String(255), nullable=True)
    
    # Status
    status = Column(String(50), default=OrderStatus.PENDING.value, index=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product_title = Column(String(255), nullable=False)
    product_price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic Schemas
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    product_title: Optional[str] = None
    product_price: Optional[float] = None
    product_image: Optional[str] = None
    
    class Config:
        from_attributes = True

class Address(BaseModel):
    name: str
    phone: str
    street: str
    city: str
    state: str
    pincode: str

class CheckoutRequest(BaseModel):
    address: Address
    payment_method: PaymentMethod

class OrderResponse(BaseModel):
    id: int
    order_number: str
    total_amount: float
    shipping_amount: float
    final_amount: float
    payment_method: str
    payment_status: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class OrderDetailResponse(OrderResponse):
    shipping_name: str
    shipping_phone: str
    shipping_address: str
    items: List[dict] = []
    
    class Config:
        from_attributes = True

# Helper to get current user ID
async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """Get current user ID from JWT token"""
    payload = verify_token(token)
    return int(payload.get("sub"))

# Helper to generate order number
def generate_order_number() -> str:
    """Generate unique order number"""
    import random
    import string
    prefix = "ORD"
    timestamp = datetime.utcnow().strftime("%Y%m%d")
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{prefix}{timestamp}{random_str}"

# Routes
@app.get("/")
async def root():
    return {"service": "Order Service", "status": "running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Cart Endpoints
@app.get("/cart", response_model=List[CartItemResponse])
async def get_cart(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get user's cart items"""
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()
    
    # TODO: Fetch product details from Product Service
    result = []
    for item in cart_items:
        result.append(CartItemResponse(
            id=item.id,
            product_id=item.product_id,
            quantity=item.quantity,
        ))
    return result

@app.post("/cart", response_model=CartItemResponse, status_code=201)
async def add_to_cart(
    item: CartItemCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Add item to cart"""
    # Check if item already in cart
    existing_item = db.query(Cart).filter(
        Cart.user_id == user_id,
        Cart.product_id == item.product_id
    ).first()
    
    if existing_item:
        existing_item.quantity += item.quantity
        existing_item.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(existing_item)
        return CartItemResponse(
            id=existing_item.id,
            product_id=existing_item.product_id,
            quantity=existing_item.quantity,
        )
    else:
        new_item = Cart(
            user_id=user_id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return CartItemResponse(
            id=new_item.id,
            product_id=new_item.product_id,
            quantity=new_item.quantity,
        )

@app.put("/cart/{item_id}")
async def update_cart_item(
    item_id: int,
    quantity: int = Query(..., gt=0),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Update cart item quantity"""
    cart_item = db.query(Cart).filter(
        Cart.id == item_id,
        Cart.user_id == user_id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    cart_item.quantity = quantity
    cart_item.updated_at = datetime.utcnow()
    db.commit()
    return {"message": "Cart item updated", "quantity": quantity}

@app.delete("/cart/{item_id}")
async def remove_from_cart(
    item_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Remove item from cart"""
    cart_item = db.query(Cart).filter(
        Cart.id == item_id,
        Cart.user_id == user_id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed from cart"}

@app.delete("/cart")
async def clear_cart(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Clear entire cart"""
    db.query(Cart).filter(Cart.user_id == user_id).delete()
    db.commit()
    return {"message": "Cart cleared"}

# Order Endpoints
@app.post("/orders", response_model=OrderResponse, status_code=201)
async def create_order(
    checkout: CheckoutRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Create order from cart"""
    # Get cart items
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()
    
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    # TODO: Fetch product details and calculate totals
    # For now, using placeholder values
    total_amount = sum(item.quantity * 100 for item in cart_items)  # Placeholder
    shipping_amount = 50.0
    discount_amount = 0.0
    final_amount = total_amount + shipping_amount - discount_amount
    
    # Create order
    order = Order(
        user_id=user_id,
        order_number=generate_order_number(),
        total_amount=total_amount,
        shipping_amount=shipping_amount,
        discount_amount=discount_amount,
        final_amount=final_amount,
        shipping_name=checkout.address.name,
        shipping_phone=checkout.address.phone,
        shipping_street=checkout.address.street,
        shipping_city=checkout.address.city,
        shipping_state=checkout.address.state,
        shipping_pincode=checkout.address.pincode,
        payment_method=checkout.payment_method.value,
        payment_status=PaymentStatus.PENDING.value,
        status=OrderStatus.PENDING.value
    )
    
    # Create Razorpay order if payment method is Razorpay
    if checkout.payment_method == PaymentMethod.RAZORPAY and RAZORPAY_ENABLED:
        try:
            razorpay_order = razorpay_client.order.create({
                'amount': int(final_amount * 100),  # Amount in paise
                'currency': 'INR',
                'receipt': order.order_number,
            })
            order.razorpay_order_id = razorpay_order['id']
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Payment gateway error: {str(e)}")
    
    db.add(order)
    db.flush()
    
    # Create order items
    for cart_item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=cart_item.product_id,
            product_title=f"Product {cart_item.product_id}",  # TODO: Fetch from Product Service
            product_price=100.0,  # TODO: Fetch from Product Service
            quantity=cart_item.quantity,
            subtotal=cart_item.quantity * 100.0
        )
        db.add(order_item)
    
    # Clear cart
    db.query(Cart).filter(Cart.user_id == user_id).delete()
    
    db.commit()
    db.refresh(order)
    
    return order

@app.get("/orders", response_model=List[OrderResponse])
async def get_orders(
    skip: int = 0,
    limit: int = 20,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get user's orders"""
    orders = db.query(Order).filter(
        Order.user_id == user_id
    ).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    
    return orders

@app.get("/orders/{order_id}", response_model=OrderDetailResponse)
async def get_order(
    order_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get order details"""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user_id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Get order items
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    items = [
        {
            "product_id": item.product_id,
            "title": item.product_title,
            "price": item.product_price,
            "quantity": item.quantity,
            "subtotal": item.subtotal
        }
        for item in order_items
    ]
    
    response = OrderDetailResponse(
        id=order.id,
        order_number=order.order_number,
        total_amount=order.total_amount,
        shipping_amount=order.shipping_amount,
        final_amount=order.final_amount,
        payment_method=order.payment_method,
        payment_status=order.payment_status,
        status=order.status,
        created_at=order.created_at,
        shipping_name=order.shipping_name,
        shipping_phone=order.shipping_phone,
        shipping_address=f"{order.shipping_street}, {order.shipping_city}, {order.shipping_state} - {order.shipping_pincode}",
        items=items
    )
    
    return response

@app.post("/orders/{order_id}/payment/verify")
async def verify_payment(
    order_id: int,
    payment_id: str,
    signature: str,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Verify Razorpay payment"""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user_id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if RAZORPAY_ENABLED:
        try:
            # Verify payment signature
            params_dict = {
                'razorpay_order_id': order.razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            razorpay_client.utility.verify_payment_signature(params_dict)
            
            # Update order
            order.payment_id = payment_id
            order.payment_status = PaymentStatus.COMPLETED.value
            order.status = OrderStatus.CONFIRMED.value
            db.commit()
            
            return {"message": "Payment verified", "order_id": order.id}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Payment verification failed: {str(e)}")
    else:
        # For testing without Razorpay
        order.payment_status = PaymentStatus.COMPLETED.value
        order.status = OrderStatus.CONFIRMED.value
        db.commit()
        return {"message": "Payment verified (test mode)", "order_id": order.id}

@app.post("/orders/{order_id}/cancel")
async def cancel_order(
    order_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Cancel an order"""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user_id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status in [OrderStatus.DELIVERED.value, OrderStatus.CANCELLED.value]:
        raise HTTPException(status_code=400, detail="Cannot cancel this order")
    
    order.status = OrderStatus.CANCELLED.value
    db.commit()
    
    return {"message": "Order cancelled", "order_id": order.id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004, reload=True)

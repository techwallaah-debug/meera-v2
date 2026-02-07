"""
Product Service - Handles product catalog, inventory, and reviews
Port: 8003
"""
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey
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

app = FastAPI(
    title="Product Service",
    version="1.0.0",
    description="Product catalog, inventory management, and reviews"
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
class ProductCategory(str, Enum):
    FASHION = "fashion"
    BEAUTY = "beauty"
    HOME = "home"
    ELECTRONICS = "electronics"
    SPORTS = "sports"
    BOOKS = "books"
    FOOD = "food"
    HEALTH = "health"

# Database Models
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    category = Column(String(50), nullable=False, index=True)
    price = Column(Float, nullable=False)
    discount_price = Column(Float, nullable=True)
    image_urls = Column(Text)  # JSON array
    stock_quantity = Column(Integer, default=0)
    sku = Column(String(100), unique=True, index=True)
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    title = Column(String(255))
    content = Column(Text)
    images = Column(Text)  # JSON array
    helpful_count = Column(Integer, default=0)
    verified_purchase = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic Schemas
class ProductCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: ProductCategory
    price: float
    discount_price: Optional[float] = None
    image_urls: List[str] = []
    stock_quantity: int = 0
    sku: str

class ProductResponse(BaseModel):
    id: int
    seller_id: int
    title: str
    description: Optional[str]
    category: str
    price: float
    discount_price: Optional[float]
    image_urls: List[str]
    stock_quantity: int
    rating: float
    review_count: int
    view_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ReviewCreate(BaseModel):
    rating: int
    title: Optional[str] = None
    content: Optional[str] = None
    images: List[str] = []

class ReviewResponse(BaseModel):
    id: int
    product_id: int
    user_id: int
    rating: int
    title: Optional[str]
    content: Optional[str]
    helpful_count: int
    verified_purchase: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Helper to get current user ID
async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """Get current user ID from JWT token"""
    payload = verify_token(token)
    return int(payload.get("sub"))

# Routes
@app.get("/")
async def root():
    return {"service": "Product Service", "status": "running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/products", response_model=ProductResponse, status_code=201)
async def create_product(
    product: ProductCreate,
    seller_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Create a new product"""
    # Check if SKU already exists
    existing_product = db.query(Product).filter(Product.sku == product.sku).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="SKU already exists")
    
    db_product = Product(
        seller_id=seller_id,
        title=product.title,
        description=product.description,
        category=product.category.value,
        price=product.price,
        discount_price=product.discount_price,
        image_urls=json.dumps(product.image_urls),
        stock_quantity=product.stock_quantity,
        sku=product.sku
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return ProductResponse(
        id=db_product.id,
        seller_id=db_product.seller_id,
        title=db_product.title,
        description=db_product.description,
        category=db_product.category,
        price=db_product.price,
        discount_price=db_product.discount_price,
        image_urls=json.loads(db_product.image_urls) if db_product.image_urls else [],
        stock_quantity=db_product.stock_quantity,
        rating=db_product.rating,
        review_count=db_product.review_count,
        view_count=db_product.view_count,
        created_at=db_product.created_at
    )

@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a product by ID"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Increment view count
    product.view_count += 1
    db.commit()
    
    return ProductResponse(
        id=product.id,
        seller_id=product.seller_id,
        title=product.title,
        description=product.description,
        category=product.category,
        price=product.price,
        discount_price=product.discount_price,
        image_urls=json.loads(product.image_urls) if product.image_urls else [],
        stock_quantity=product.stock_quantity,
        rating=product.rating,
        review_count=product.review_count,
        view_count=product.view_count,
        created_at=product.created_at
    )

@app.get("/products", response_model=List[ProductResponse])
async def search_products(
    q: Optional[str] = Query(None, description="Search query"),
    category: Optional[ProductCategory] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Search and filter products"""
    query = db.query(Product).filter(Product.is_active == True)
    
    if q:
        query = query.filter(Product.title.like(f"%{q}%"))
    if category:
        query = query.filter(Product.category == category.value)
    if min_price:
        query = query.filter(Product.price >= min_price)
    if max_price:
        query = query.filter(Product.price <= max_price)
    
    products = query.order_by(Product.created_at.desc()).offset(skip).limit(limit).all()
    
    result = []
    for product in products:
        result.append(ProductResponse(
            id=product.id,
            seller_id=product.seller_id,
            title=product.title,
            description=product.description,
            category=product.category,
            price=product.price,
            discount_price=product.discount_price,
            image_urls=json.loads(product.image_urls) if product.image_urls else [],
            stock_quantity=product.stock_quantity,
            rating=product.rating,
            review_count=product.review_count,
            view_count=product.view_count,
            created_at=product.created_at
        ))
    return result

@app.post("/products/{product_id}/reviews", response_model=ReviewResponse, status_code=201)
async def create_review(
    product_id: int,
    review: ReviewCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Create a product review"""
    if review.rating < 1 or review.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if user already reviewed this product
    existing_review = db.query(Review).filter(
        Review.product_id == product_id,
        Review.user_id == user_id
    ).first()
    
    if existing_review:
        raise HTTPException(status_code=400, detail="You have already reviewed this product")
    
    db_review = Review(
        product_id=product_id,
        user_id=user_id,
        rating=review.rating,
        title=review.title,
        content=review.content,
        images=json.dumps(review.images)
    )
    db.add(db_review)
    
    # Update product rating
    product.review_count += 1
    new_rating = ((product.rating * (product.review_count - 1)) + review.rating) / product.review_count
    product.rating = round(new_rating, 2)
    
    db.commit()
    db.refresh(db_review)
    
    return ReviewResponse(
        id=db_review.id,
        product_id=db_review.product_id,
        user_id=db_review.user_id,
        rating=db_review.rating,
        title=db_review.title,
        content=db_review.content,
        helpful_count=db_review.helpful_count,
        verified_purchase=db_review.verified_purchase,
        created_at=db_review.created_at
    )

@app.get("/products/{product_id}/reviews", response_model=List[ReviewResponse])
async def get_reviews(
    product_id: int,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get reviews for a product"""
    reviews = db.query(Review).filter(
        Review.product_id == product_id
    ).order_by(Review.created_at.desc()).offset(skip).limit(limit).all()
    
    return [
        ReviewResponse(
            id=r.id,
            product_id=r.product_id,
            user_id=r.user_id,
            rating=r.rating,
            title=r.title,
            content=r.content,
            helpful_count=r.helpful_count,
            verified_purchase=r.verified_purchase,
            created_at=r.created_at
        ) for r in reviews
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003, reload=True)

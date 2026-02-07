# AI-Powered Social Commerce Platform
## Complete Technical Documentation for Cursor AI
**Version:** 2.0  
**Last Updated:** February 6, 2026  
**Development Environment:** Cursor AI Pro  
**Target:** 16-Week MVP

## Table of Contents
1. [System Architecture Overview](#1-system-architecture-overview)
2. [Technology Stack](#2-technology-stack)
3. [Development Environment Setup](#3-development-environment-setup)
4. [Backend Implementation](#4-backend-implementation)
5. [Frontend Implementation](#5-frontend-implementation)
6. [AI/ML Services](#6-aiml-services)
7. [Database Schema](#7-database-schema)
8. [API Documentation](#8-api-documentation)
9. [Authentication & Security](#9-authentication--security)
10. [Third-Party Integrations](#10-third-party-integrations)
11. [DevOps & Deployment](#11-devops--deployment)
12. [Testing Strategy](#12-testing-strategy)
13. [16-Week Sprint Plan](#13-16-week-sprint-plan)
14. [Cursor AI Optimization](#14-cursor-ai-optimization)

---

## 1. System Architecture Overview

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                            │
├─────────────────────────────────────────────────────────────┤
│  React Native App (iOS/Android)  │   Next.js Web App        │
└─────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    API GATEWAY (Kong)                       │
│  • Rate Limiting  • Auth  • Routing  • Load Balancing      │
└─────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  MICROSERVICES LAYER                        │
├──────────────┬──────────────┬──────────────┬───────────────┤
│ User Service │Content Service│Product Service│Order Service │
│  Port: 8001  │  Port: 8002  │  Port: 8003  │  Port: 8004  │
├──────────────┼──────────────┼──────────────┼───────────────┤
│Search Service│Recommendation│Analytics Svc │Notification   │
│  Port: 8005  │  Port: 8006  │  Port: 8007  │  Port: 8008  │
└─────────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                     DATA LAYER                              │
├────────────────┬───────────────┬───────────────┬────────────┤
│    MySQL       │    Redis      │ Elasticsearch │  Pinecone  │
│(Primary Data)  │  (Cache)      │(Text Search)  │ (Vectors)  │
└────────────────┴───────────────┴───────────────┴────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  EXTERNAL SERVICES                          │
├────────────────┬───────────────┬──────────────┬─────────────┤
│  AWS S3        │  Razorpay     │ OpenAI GPT-4 │ Shiprocket  │
│ (Media)        │ (Payments)    │ (AI)         │ (Logistics) │
└────────────────┴───────────────┴──────────────┴─────────────┘
```

### 1.2 Microservices Breakdown

#### User Service (Port 8001)
- User registration, login, JWT management
- Profile management (bio, avatar, preferences)
- Social graph (follow/unfollow, followers/following)
- User settings and preferences

#### Content Service (Port 8002)
- Post creation, editing, deletion
- Media upload (images, videos)
- Comments and replies
- Likes, saves, shares
- Feed generation (chronological + algorithmic)

#### Product Service (Port 8003)
- Product catalog management
- Inventory tracking
- Product search and filtering
- Reviews and ratings
- Seller management

#### Order Service (Port 8004)
- Shopping cart
- Checkout and order placement
- Payment processing integration
- Order tracking
- Returns and refunds

#### Search Service (Port 8005)
- Full-text search (Elasticsearch)
- Visual search (image similarity)
- Autocomplete and suggestions
- Search analytics

#### Recommendation Service (Port 8006)
- Personalized feed ranking
- Product recommendations
- Similar item suggestions
- Trending content detection

#### Analytics Service (Port 8007)
- Event tracking
- User behavior analytics
- Business metrics (GMV, conversion)
- Creator analytics dashboard

#### Notification Service (Port 8008)
- Push notifications (Firebase)
- Email notifications (SendGrid)
- SMS notifications (Twilio)
- In-app notifications

---

## 2. Technology Stack

### 2.1 Frontend

#### Mobile App
```json
{
  "framework": "React Native 0.73",
  "language": "TypeScript 5.3",
  "state": "Zustand 4.5",
  "navigation": "React Navigation 6",
  "ui": "React Native Paper + Custom Components",
  "networking": "Axios + React Query",
  "storage": "AsyncStorage",
  "media": "React Native Image Picker, Video",
  "ar": "React Native AR (ARKit/ARCore wrapper)"
}
```

#### Web App (Admin/SEO)
```json
{
  "framework": "Next.js 14",
  "language": "TypeScript 5.3",
  "styling": "Tailwind CSS 3.4",
  "state": "Zustand 4.5",
  "forms": "React Hook Form + Zod"
}
```

### 2.2 Backend

#### API Services
```json
{
  "framework": "FastAPI 0.109",
  "language": "Python 3.11",
  "async": "async/await with uvicorn",
  "orm": "SQLAlchemy 2.0",
  "migrations": "Alembic",
  "validation": "Pydantic V2",
  "testing": "pytest + httpx"
}
```

### 2.3 Databases & Caching

**Primary Database:**
- MySQL 8.0
- Purpose: Users, products, orders, content
- HA: Master-replica setup

**Cache Layer:**
- Redis 7.2
- Purpose: Sessions, feed cache, rate limiting
- Persistence: RDB snapshots

**Search Engine:**
- Elasticsearch 8.11
- Purpose: Product/content full-text search
- Cluster: 3-node for HA

**Vector Database:**
- Pinecone (managed)
- Purpose: Visual search, embeddings
- Index: ~100M vectors

**Analytics:**
- ClickHouse 23.8
- Purpose: Event tracking, fast aggregations
- Retention: 1 year hot, 3 years cold

### 2.4 AI/ML Stack

**Training:**
- Framework: PyTorch 2.1
- Environment: AWS EC2 g5.2xlarge (GPU)
- Experiment Tracking: MLflow

**Inference:**
- Serving: TorchServe or FastAPI endpoint
- Optimization: ONNX Runtime, TensorRT
- Scaling: Auto-scaling based on traffic

**Computer Vision:**
- Feature Extraction: ResNet-50, ViT-B/16
- Segmentation: U2-Net
- Similarity: FAISS for fast vector search

**NLP:**
- LLM: OpenAI GPT-4 API (initially)
- Fine-tuning: LoRA on Llama 2 (future)
- Embeddings: Sentence-BERT

**Recommendation:**
- Algorithm: Two-Tower Neural Network
- Features: User history, product attributes, context
- Update: Batch daily + real-time personalization

### 2.5 Infrastructure

**Cloud Provider:** AWS
- Region: ap-south-1 (Mumbai)
- Multi-AZ deployment

**Compute:**
- EKS (Kubernetes) for microservices
- EC2 for ML training
- Lambda for serverless functions

**Storage:**
- S3: Media files, backups
- EBS: Database volumes
- CloudFront CDN: Fast media delivery

**Networking:**
- VPC with private/public subnets
- ALB (Application Load Balancer)
- Route 53 for DNS

**Monitoring:**
- CloudWatch for metrics
- Datadog for APM
- Sentry for error tracking
- ELK for log aggregation

---

## 3. Development Environment Setup

### 3.1 Prerequisites

```bash
# Install required tools
- Node.js 20 LTS
- Python 3.11+
- Docker & Docker Compose
- MySQL 8.0
- Redis 7
- Git
- Cursor IDE (with AI enabled)
```

### 3.2 Project Structure

```
social-commerce-platform/
├── backend/
│   ├── services/
│   │   ├── user-service/
│   │   ├── content-service/
│   │   ├── product-service/
│   │   ├── order-service/
│   │   ├── search-service/
│   │   ├── recommendation-service/
│   │   ├── analytics-service/
│   │   └── notification-service/
│   ├── shared/
│   │   ├── database/
│   │   ├── auth/
│   │   └── utils/
│   └── ml/
│       ├── recommendation/
│       ├── visual-search/
│       ├── content-generation/
│       └── models/
├── frontend/
│   ├── mobile/
│   │   ├── src/
│   │   │   ├── screens/
│   │   │   ├── components/
│   │   │   ├── navigation/
│   │   │   ├── store/
│   │   │   ├── services/
│   │   │   └── utils/
│   │   ├── ios/
│   │   └── android/
│   └── web/
│       ├── app/
│       ├── components/
│       └── public/
├── infrastructure/
│   ├── docker/
│   ├── kubernetes/
│   ├── terraform/
│   └── ci-cd/
├── docs/
└── tests/
```

### 3.3 Local Development Setup

#### Step 1: Clone and Setup

```bash
# Create project directory
mkdir social-commerce-platform
cd social-commerce-platform

# Initialize git
git init

# Create virtual environment for Python
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install fastapi uvicorn sqlalchemy pymysql cryptography pydantic python-jose bcrypt
```

#### Step 2: Docker Compose for Local Services

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: social_commerce
      MYSQL_USER: admin
      MYSQL_PASSWORD: password
      MYSQL_ROOT_PASSWORD: rootpassword
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    command: --default-authentication-plugin=mysql_native_password

  redis:
    image: redis:7.2-alpine
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
    volumes:
      - es_data:/usr/share/elasticsearch/data

  mailhog:
    image: mailhog/mailhog
    ports:
      - "1025:1025"  # SMTP
      - "8025:8025"  # Web UI

volumes:
  mysql_data:
  redis_data:
  es_data:
```

```bash
# Start all services
docker-compose up -d

# Verify services are running
docker-compose ps
```

#### Step 3: Environment Variables

Create `.env` file:

```env
# Database
DATABASE_URL=mysql+pymysql://admin:password@localhost:3306/social_commerce

# Redis
REDIS_URL=redis://localhost:6379

# JWT Secret
JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AWS (for development, use localstack or actual credentials)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=ap-south-1
S3_BUCKET_NAME=social-commerce-dev

# OpenAI
OPENAI_API_KEY=sk-your-openai-key

# Razorpay
RAZORPAY_KEY_ID=rzp_test_your-key
RAZORPAY_KEY_SECRET=your-secret

# SendGrid
SENDGRID_API_KEY=SG.your-sendgrid-key

# Environment
ENVIRONMENT=development
DEBUG=True
```

---

## 4. Backend Implementation

### 4.1 User Service

**File:** `services/user-service/src/main.py`

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os

# FastAPI app
app = FastAPI(title="User Service", version="1.0")

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://admin:password@localhost:3306/social_commerce")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)
    bio = Column(Text)
    avatar_url = Column(String)
    is_creator = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# Schemas
class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=30)
    full_name: str
    password: str = Field(..., min_length=8)
    is_creator: bool = False

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str
    bio: Optional[str]
    avatar_url: Optional[str]
    is_creator: bool
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user is None:
        raise credentials_exception
    return user

# Routes
@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password,
        is_creator=user.is_creator
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/me", response_model=UserResponse)
async def update_user(
    full_name: Optional[str] = None,
    bio: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if full_name:
        current_user.full_name = full_name
    if bio:
        current_user.bio = bio
    current_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(current_user)
    return current_user

@app.post("/users/{user_id}/follow")
async def follow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # TODO: Implement follow relationship in separate table
    return {"message": "Followed successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

**Running User Service:**
```bash
cd services/user-service
python src/main.py

# Test the API
curl http://localhost:8001/docs  # Swagger UI
```

### 4.2 Content Service

**File:** `services/content-service/src/main.py`

```python
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import os
import boto3
from uuid import uuid4

app = FastAPI(title="Content Service", version="1.0")

# Database
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# AWS S3 setup
s3_client = boto3.client('s3', region_name=os.getenv('AWS_REGION'))
S3_BUCKET = os.getenv('S3_BUCKET_NAME')

# Models
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    caption = Column(Text)
    media_urls = Column(Text)  # JSON array of media URLs
    product_tags = Column(Text)  # JSON array of product IDs
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    parent_id = Column(Integer, ForeignKey('comments.id'), nullable=True)
    like_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class Like(Base):
    __tablename__ = "likes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=True)
    comment_id = Column(Integer, ForeignKey('comments.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# Schemas
class PostCreate(BaseModel):
    caption: Optional[str] = None
    media_urls: List[str] = []
    product_tags: List[int] = []

class PostResponse(BaseModel):
    id: int
    user_id: int
    caption: Optional[str]
    media_urls: List[str]
    like_count: int
    comment_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    content: str
    parent_id: Optional[int] = None

class CommentResponse(BaseModel):
    id: int
    post_id: int
    user_id: int
    content: str
    like_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.post("/posts", response_model=PostResponse)
async def create_post(post: PostCreate, user_id: int, db: Session = Depends(get_db)):
    # In production, get user_id from JWT token
    import json
    db_post = Post(
        user_id=user_id,
        caption=post.caption,
        media_urls=json.dumps(post.media_urls),
        product_tags=json.dumps(post.product_tags)
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    # Convert JSON strings back to lists for response
    response_data = PostResponse.from_orm(db_post)
    response_data.media_urls = json.loads(db_post.media_urls) if db_post.media_urls else []
    return response_data

@app.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    import json
    response_data = PostResponse.from_orm(post)
    response_data.media_urls = json.loads(post.media_urls) if post.media_urls else []
    return response_data

@app.get("/posts", response_model=List[PostResponse])
async def get_feed(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    posts = db.query(Post).filter(Post.is_published == True).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()
    
    import json
    result = []
    for post in posts:
        response_data = PostResponse.from_orm(post)
        response_data.media_urls = json.loads(post.media_urls) if post.media_urls else []
        result.append(response_data)
    return result

@app.post("/posts/{post_id}/like")
async def like_post(post_id: int, user_id: int, db: Session = Depends(get_db)):
    # Check if post exists
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check if already liked
    existing_like = db.query(Like).filter(Like.user_id == user_id, Like.post_id == post_id).first()
    if existing_like:
        # Unlike
        db.delete(existing_like)
        post.like_count -= 1
    else:
        # Like
        new_like = Like(user_id=user_id, post_id=post_id)
        db.add(new_like)
        post.like_count += 1
    
    db.commit()
    return {"liked": existing_like is None, "like_count": post.like_count}

@app.post("/posts/{post_id}/comments", response_model=CommentResponse)
async def create_comment(post_id: int, comment: CommentCreate, user_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db_comment = Comment(
        post_id=post_id,
        user_id=user_id,
        content=comment.content,
        parent_id=comment.parent_id
    )
    db.add(db_comment)
    post.comment_count += 1
    db.commit()
    db.refresh(db_comment)
    
    return db_comment

@app.get("/posts/{post_id}/comments", response_model=List[CommentResponse])
async def get_comments(post_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.post_id == post_id, Comment.parent_id == None).all()
    return comments

@app.post("/upload-media")
async def upload_media(file: UploadFile = File(...)):
    # Generate unique filename
    file_extension = file.filename.split('.')[-1]
    unique_filename = f"{uuid4()}.{file_extension}"
    
    # Upload to S3
    try:
        s3_client.upload_fileobj(
            file.file,
            S3_BUCKET,
            f"posts/{unique_filename}",
            ExtraArgs={'ContentType': file.content_type}
        )
        
        media_url = f"https://{S3_BUCKET}.s3.amazonaws.com/posts/{unique_filename}"
        return {"media_url": media_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
```

### 4.3 Product Service

**File:** `services/product-service/src/main.py`

```python
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum
import os

app = FastAPI(title="Product Service", version="1.0")

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Enums
class ProductCategory(str, Enum):
    FASHION = "fashion"
    BEAUTY = "beauty"
    HOME = "home"
    ELECTRONICS = "electronics"
    SPORTS = "sports"
    BOOKS = "books"

# Models
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    discount_price = Column(Float, nullable=True)
    image_urls = Column(Text)  # JSON array
    stock_quantity = Column(Integer, default=0)
    sku = Column(String, unique=True, index=True)
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    title = Column(String)
    content = Column(Text)
    images = Column(Text)  # JSON array
    helpful_count = Column(Integer, default=0)
    verified_purchase = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# Schemas
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

# Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.post("/products", response_model=ProductResponse)
async def create_product(product: ProductCreate, seller_id: int, db: Session = Depends(get_db)):
    import json
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
    
    response_data = ProductResponse.from_orm(db_product)
    response_data.image_urls = json.loads(db_product.image_urls) if db_product.image_urls else []
    return response_data

@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Increment view count
    product.view_count += 1
    db.commit()
    
    import json
    response_data = ProductResponse.from_orm(product)
    response_data.image_urls = json.loads(product.image_urls) if product.image_urls else []
    return response_data

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
    query = db.query(Product).filter(Product.is_active == True)
    
    if q:
        query = query.filter(Product.title.ilike(f"%{q}%"))
    if category:
        query = query.filter(Product.category == category.value)
    if min_price:
        query = query.filter(Product.price >= min_price)
    if max_price:
        query = query.filter(Product.price <= max_price)
    
    products = query.offset(skip).limit(limit).all()
    
    import json
    result = []
    for product in products:
        response_data = ProductResponse.from_orm(product)
        response_data.image_urls = json.loads(product.image_urls) if product.image_urls else []
        result.append(response_data)
    return result

@app.post("/products/{product_id}/reviews", response_model=ReviewResponse)
async def create_review(
    product_id: int,
    review: ReviewCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    import json
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
    
    return db_review

@app.get("/products/{product_id}/reviews", response_model=List[ReviewResponse])
async def get_reviews(product_id: int, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.product_id == product_id).offset(skip).limit(limit).all()
    return reviews

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
```

---

## 5. Frontend Implementation

*[To be continued...]*

---

## 6. AI/ML Services

*[To be continued...]*

---

## 7. Database Schema

*[To be continued...]*

---

## 8. API Documentation

*[To be continued...]*

---

## 9. Authentication & Security

*[To be continued...]*

---

## 10. Third-Party Integrations

*[To be continued...]*

---

## 11. DevOps & Deployment

*[To be continued...]*

---

## 12. Testing Strategy

*[To be continued...]*

---

## 13. 16-Week Sprint Plan

*[To be continued...]*

---

## 14. Cursor AI Optimization

*[To be continued...]*

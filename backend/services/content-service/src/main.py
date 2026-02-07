"""
Content Service - Handles posts, comments, likes, and media uploads
Port: 8002
"""
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import os
import json
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from shared.database.connection import get_db, Base, engine
from shared.auth.jwt import verify_token
from fastapi.security import OAuth2PasswordBearer

# AWS S3 setup (optional - can use local storage for dev)
try:
    import boto3
    s3_client = boto3.client('s3', region_name=os.getenv('AWS_REGION', 'ap-south-1'))
    S3_BUCKET = os.getenv('S3_BUCKET_NAME', 'social-commerce-dev')
    USE_S3 = True
except:
    USE_S3 = False
    UPLOAD_DIR = "uploads/posts"

from uuid import uuid4

app = FastAPI(
    title="Content Service",
    version="1.0.0",
    description="Post creation, comments, likes, and media management"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Database Models
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    caption = Column(Text)
    media_urls = Column(Text)  # JSON array of media URLs
    product_tags = Column(Text)  # JSON array of product IDs
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    parent_id = Column(Integer, ForeignKey('comments.id'), nullable=True)
    like_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class Like(Base):
    __tablename__ = "likes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=True, index=True)
    comment_id = Column(Integer, ForeignKey('comments.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic Schemas
class PostCreate(BaseModel):
    caption: Optional[str] = None
    media_urls: List[str] = []
    product_tags: List[int] = []

class PostResponse(BaseModel):
    id: int
    user_id: int
    caption: Optional[str]
    media_urls: List[str]
    product_tags: List[int]
    like_count: int
    comment_count: int
    share_count: int
    view_count: int
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
    parent_id: Optional[int]
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
    return {"service": "Content Service", "status": "running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/posts", response_model=PostResponse, status_code=201)
async def create_post(
    post: PostCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Create a new post"""
    db_post = Post(
        user_id=user_id,
        caption=post.caption,
        media_urls=json.dumps(post.media_urls),
        product_tags=json.dumps(post.product_tags)
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    response_data = PostResponse(
        id=db_post.id,
        user_id=db_post.user_id,
        caption=db_post.caption,
        media_urls=json.loads(db_post.media_urls) if db_post.media_urls else [],
        product_tags=json.loads(db_post.product_tags) if db_post.product_tags else [],
        like_count=db_post.like_count,
        comment_count=db_post.comment_count,
        share_count=db_post.share_count,
        view_count=db_post.view_count,
        created_at=db_post.created_at
    )
    return response_data

@app.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    """Get a post by ID"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Increment view count
    post.view_count += 1
    db.commit()
    
    response_data = PostResponse(
        id=post.id,
        user_id=post.user_id,
        caption=post.caption,
        media_urls=json.loads(post.media_urls) if post.media_urls else [],
        product_tags=json.loads(post.product_tags) if post.product_tags else [],
        like_count=post.like_count,
        comment_count=post.comment_count,
        share_count=post.share_count,
        view_count=post.view_count,
        created_at=post.created_at
    )
    return response_data

@app.get("/posts", response_model=List[PostResponse])
async def get_feed(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Get feed of posts"""
    posts = db.query(Post).filter(
        Post.is_published == True
    ).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()
    
    result = []
    for post in posts:
        result.append(PostResponse(
            id=post.id,
            user_id=post.user_id,
            caption=post.caption,
            media_urls=json.loads(post.media_urls) if post.media_urls else [],
            product_tags=json.loads(post.product_tags) if post.product_tags else [],
            like_count=post.like_count,
            comment_count=post.comment_count,
            share_count=post.share_count,
            view_count=post.view_count,
            created_at=post.created_at
        ))
    return result

@app.post("/posts/{post_id}/like")
async def like_post(
    post_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Like or unlike a post"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    existing_like = db.query(Like).filter(
        Like.user_id == user_id,
        Like.post_id == post_id
    ).first()
    
    if existing_like:
        # Unlike
        db.delete(existing_like)
        post.like_count = max(0, post.like_count - 1)
        liked = False
    else:
        # Like
        new_like = Like(user_id=user_id, post_id=post_id)
        db.add(new_like)
        post.like_count += 1
        liked = True
    
    db.commit()
    return {"liked": liked, "like_count": post.like_count}

@app.post("/posts/{post_id}/comments", response_model=CommentResponse, status_code=201)
async def create_comment(
    post_id: int,
    comment: CommentCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Create a comment on a post"""
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
    
    return CommentResponse(
        id=db_comment.id,
        post_id=db_comment.post_id,
        user_id=db_comment.user_id,
        content=db_comment.content,
        like_count=db_comment.like_count,
        parent_id=db_comment.parent_id,
        created_at=db_comment.created_at
    )

@app.get("/posts/{post_id}/comments", response_model=List[CommentResponse])
async def get_comments(
    post_id: int,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get comments for a post"""
    comments = db.query(Comment).filter(
        Comment.post_id == post_id,
        Comment.parent_id == None
    ).order_by(Comment.created_at.desc()).offset(skip).limit(limit).all()
    
    return [
        CommentResponse(
            id=c.id,
            post_id=c.post_id,
            user_id=c.user_id,
            content=c.content,
            like_count=c.like_count,
            parent_id=c.parent_id,
            created_at=c.created_at
        ) for c in comments
    ]

@app.post("/upload-media")
async def upload_media(
    file: UploadFile = File(...),
    user_id: int = Depends(get_current_user_id)
):
    """Upload media file (image/video)"""
    # Generate unique filename
    file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'bin'
    unique_filename = f"{uuid4()}.{file_extension}"
    
    if USE_S3:
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
    else:
        # Local storage (for development)
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        media_url = f"/uploads/posts/{unique_filename}"
        return {"media_url": media_url}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002, reload=True)

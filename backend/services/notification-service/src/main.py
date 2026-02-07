"""
Notification Service - Handles push, email, and SMS notifications
Port: 8008
"""
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Enum as SQLEnum
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum
import os
import sys
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from shared.database.connection import get_db, Base, engine
from shared.auth.jwt import verify_token
from fastapi.security import OAuth2PasswordBearer

# SendGrid for emails
try:
    import sendgrid
    from sendgrid.helpers.mail import Mail
    sg_client = sendgrid.SendGridAPIClient(os.getenv('SENDGRID_API_KEY', ''))
    SENDGRID_ENABLED = True
except:
    SENDGRID_ENABLED = False

# Twilio for SMS
try:
    from twilio.rest import Client
    twilio_client = Client(
        os.getenv('TWILIO_ACCOUNT_SID', ''),
        os.getenv('TWILIO_AUTH_TOKEN', '')
    )
    TWILIO_ENABLED = True
except:
    TWILIO_ENABLED = False

# Firebase for push notifications (would need firebase-admin SDK)
FIREBASE_ENABLED = False  # TODO: Implement Firebase

app = FastAPI(
    title="Notification Service",
    version="1.0.0",
    description="Push, email, and SMS notifications"
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
class NotificationType(str, Enum):
    PUSH = "push"
    EMAIL = "email"
    SMS = "sms"
    IN_APP = "in_app"

class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    READ = "read"

# Database Models
class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    data = Column(Text)  # JSON data
    status = Column(String(50), default=NotificationStatus.PENDING.value)
    read_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

Base.metadata.create_all(bind=engine)

# Schemas
class NotificationCreate(BaseModel):
    user_id: int
    type: NotificationType
    title: str
    message: str
    data: Optional[dict] = None

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    type: str
    title: str
    message: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Helper functions
async def send_email_notification(to_email: str, subject: str, content: str):
    """Send email via SendGrid"""
    if not SENDGRID_ENABLED:
        print(f"[EMAIL] Would send to {to_email}: {subject}")
        return False
    
    try:
        message = Mail(
            from_email=os.getenv('SENDGRID_FROM_EMAIL', 'noreply@socialcommerce.com'),
            to_emails=to_email,
            subject=subject,
            html_content=content
        )
        response = sg_client.send(message)
        return response.status_code == 202
    except Exception as e:
        print(f"Email send error: {e}")
        return False

async def send_sms_notification(to_phone: str, message: str):
    """Send SMS via Twilio"""
    if not TWILIO_ENABLED:
        print(f"[SMS] Would send to {to_phone}: {message}")
        return False
    
    try:
        twilio_client.messages.create(
            body=message,
            from_=os.getenv('TWILIO_PHONE_NUMBER', ''),
            to=to_phone
        )
        return True
    except Exception as e:
        print(f"SMS send error: {e}")
        return False

async def send_push_notification(user_id: int, title: str, message: str, data: dict = None):
    """Send push notification via Firebase"""
    if not FIREBASE_ENABLED:
        print(f"[PUSH] Would send to user {user_id}: {title} - {message}")
        return False
    
    # TODO: Implement Firebase Cloud Messaging
    return False

# Routes
@app.get("/")
async def root():
    return {
        "service": "Notification Service",
        "status": "running",
        "version": "1.0.0",
        "email": "enabled" if SENDGRID_ENABLED else "disabled",
        "sms": "enabled" if TWILIO_ENABLED else "disabled",
        "push": "enabled" if FIREBASE_ENABLED else "disabled"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/notifications", response_model=NotificationResponse, status_code=201)
async def create_notification(
    notification: NotificationCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create and send a notification"""
    # Save notification to database
    db_notification = Notification(
        user_id=notification.user_id,
        type=notification.type.value,
        title=notification.title,
        message=notification.message,
        data=json.dumps(notification.data) if notification.data else None,
        status=NotificationStatus.PENDING.value
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    
    # Send notification in background
    if notification.type == NotificationType.EMAIL:
        # TODO: Get user email from User Service
        background_tasks.add_task(
            send_email_notification,
            f"user{notification.user_id}@example.com",
            notification.title,
            notification.message
        )
    elif notification.type == NotificationType.SMS:
        # TODO: Get user phone from User Service
        background_tasks.add_task(
            send_sms_notification,
            "+1234567890",
            notification.message
        )
    elif notification.type == NotificationType.PUSH:
        background_tasks.add_task(
            send_push_notification,
            notification.user_id,
            notification.title,
            notification.message,
            notification.data
        )
    
    # Update status
    db_notification.status = NotificationStatus.SENT.value
    db.commit()
    
    return NotificationResponse(
        id=db_notification.id,
        user_id=db_notification.user_id,
        type=db_notification.type,
        title=db_notification.title,
        message=db_notification.message,
        status=db_notification.status,
        created_at=db_notification.created_at
    )

@app.get("/notifications", response_model=List[NotificationResponse])
async def get_notifications(
    user_id: int,
    skip: int = 0,
    limit: int = 20,
    unread_only: bool = False,
    db: Session = Depends(get_db)
):
    """Get user notifications"""
    query = db.query(Notification).filter(Notification.user_id == user_id)
    
    if unread_only:
        query = query.filter(Notification.read_at == None)
    
    notifications = query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
    
    return [
        NotificationResponse(
            id=n.id,
            user_id=n.user_id,
            type=n.type,
            title=n.title,
            message=n.message,
            status=n.status,
            created_at=n.created_at
        )
        for n in notifications
    ]

@app.put("/notifications/{notification_id}/read")
async def mark_as_read(
    notification_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Mark notification as read"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == user_id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.read_at = datetime.utcnow()
    notification.status = NotificationStatus.READ.value
    db.commit()
    
    return {"message": "Notification marked as read"}

@app.get("/notifications/unread/count")
async def get_unread_count(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get unread notification count"""
    count = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.read_at == None
    ).count()
    
    return {"count": count}

# Helper to get current user ID
async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """Get current user ID from JWT token"""
    payload = verify_token(token)
    return int(payload.get("sub"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8008, reload=True)

"""
Analytics Service - Event tracking and analytics
Port: 8007
"""
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, JSON
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import os
import sys
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from shared.database.connection import get_db, Base, engine
from shared.auth.jwt import verify_token
from fastapi.security import OAuth2PasswordBearer

app = FastAPI(
    title="Analytics Service",
    version="1.0.0",
    description="Event tracking, user behavior analytics, and business metrics"
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
class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=True)
    event_type = Column(String(100), nullable=False, index=True)
    event_name = Column(String(255), nullable=False, index=True)
    properties = Column(JSON)  # JSON data
    session_id = Column(String(255), index=True)
    ip_address = Column(String(50))
    user_agent = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class Metric(Base):
    __tablename__ = "metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String(100), nullable=False, index=True)
    metric_value = Column(Float, nullable=False)
    metric_type = Column(String(50))  # counter, gauge, histogram
    tags = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

Base.metadata.create_all(bind=engine)

# Schemas
class EventCreate(BaseModel):
    event_type: str
    event_name: str
    properties: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None

class EventResponse(BaseModel):
    id: int
    event_type: str
    event_name: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class AnalyticsResponse(BaseModel):
    total_events: int
    unique_users: int
    events_by_type: Dict[str, int]
    time_range: str

# Helper to get current user ID
async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """Get current user ID from JWT token"""
    payload = verify_token(token)
    return int(payload.get("sub"))

# Routes
@app.get("/")
async def root():
    return {
        "service": "Analytics Service",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/events", response_model=EventResponse, status_code=201)
async def track_event(
    event: EventCreate,
    user_id: Optional[int] = Depends(get_current_user_id),
    request: Any = None,
    db: Session = Depends(get_db)
):
    """Track an event"""
    # Get IP and user agent from request
    ip_address = None
    user_agent = None
    if request:
        ip_address = request.client.host if hasattr(request, 'client') else None
        user_agent = request.headers.get('user-agent')
    
    db_event = Event(
        user_id=user_id,
        event_type=event.event_type,
        event_name=event.event_name,
        properties=json.dumps(event.properties) if event.properties else None,
        session_id=event.session_id,
        ip_address=ip_address,
        user_agent=user_agent
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    return EventResponse(
        id=db_event.id,
        event_type=db_event.event_type,
        event_name=db_event.event_name,
        created_at=db_event.created_at
    )

@app.get("/events", response_model=List[EventResponse])
async def get_events(
    event_type: Optional[str] = None,
    user_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get events with filters"""
    query = db.query(Event)
    
    if event_type:
        query = query.filter(Event.event_type == event_type)
    if user_id:
        query = query.filter(Event.user_id == user_id)
    if start_date:
        query = query.filter(Event.created_at >= start_date)
    if end_date:
        query = query.filter(Event.created_at <= end_date)
    
    events = query.order_by(Event.created_at.desc()).offset(skip).limit(limit).all()
    
    return [
        EventResponse(
            id=e.id,
            event_type=e.event_type,
            event_name=e.event_name,
            created_at=e.created_at
        )
        for e in events
    ]

@app.get("/analytics/overview", response_model=AnalyticsResponse)
async def get_analytics_overview(
    days: int = Query(7, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get analytics overview"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    events = db.query(Event).filter(Event.created_at >= start_date).all()
    
    total_events = len(events)
    unique_users = len(set(e.user_id for e in events if e.user_id))
    
    events_by_type = {}
    for event in events:
        events_by_type[event.event_type] = events_by_type.get(event.event_type, 0) + 1
    
    return AnalyticsResponse(
        total_events=total_events,
        unique_users=unique_users,
        events_by_type=events_by_type,
        time_range=f"Last {days} days"
    )

@app.get("/analytics/user/{user_id}")
async def get_user_analytics(
    user_id: int,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get analytics for a specific user"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    events = db.query(Event).filter(
        Event.user_id == user_id,
        Event.created_at >= start_date
    ).all()
    
    events_by_type = {}
    for event in events:
        events_by_type[event.event_type] = events_by_type.get(event.event_type, 0) + 1
    
    return {
        "user_id": user_id,
        "total_events": len(events),
        "events_by_type": events_by_type,
        "time_range": f"Last {days} days"
    }

@app.get("/analytics/business")
async def get_business_metrics(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get business metrics (GMV, conversion, etc.)"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # TODO: Query actual order data from Order Service
    # For now, return placeholder metrics
    
    return {
        "gmv": 0,  # Gross Merchandise Value
        "orders": 0,
        "revenue": 0,
        "conversion_rate": 0.0,
        "average_order_value": 0.0,
        "time_range": f"Last {days} days"
    }

@app.get("/analytics/products")
async def get_product_analytics(
    product_id: Optional[int] = None,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get product analytics"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # TODO: Query product views, purchases, etc.
    
    return {
        "product_id": product_id,
        "views": 0,
        "purchases": 0,
        "conversion_rate": 0.0,
        "time_range": f"Last {days} days"
    }

@app.post("/metrics")
async def record_metric(
    metric_name: str,
    metric_value: float,
    metric_type: str = "counter",
    tags: Optional[Dict[str, str]] = None,
    db: Session = Depends(get_db)
):
    """Record a metric"""
    db_metric = Metric(
        metric_name=metric_name,
        metric_value=metric_value,
        metric_type=metric_type,
        tags=json.dumps(tags) if tags else None
    )
    db.add(db_metric)
    db.commit()
    
    return {"message": "Metric recorded", "metric_id": db_metric.id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8007, reload=True)

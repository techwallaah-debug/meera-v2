"""
Base model with common fields
"""
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime
from .connection import Base


class BaseModel(Base):
    """
    Abstract base model with common fields
    All models should inherit from this
    """
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    @declared_attr
    def __tablename__(cls):
        """Auto-generate table name from class name"""
        return cls.__name__.lower() + 's'

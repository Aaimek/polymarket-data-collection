from sqlalchemy import (
    Column,
    String,
    Text,
    Boolean,
    Numeric,
    TIMESTAMP
)
from sqlalchemy.orm import relationship
from .base import Base

class Event(Base):
    __tablename__ = 'events'
    
    id = Column(String, primary_key=True)
    ticker = Column(String, nullable=False)
    slug = Column(String, nullable=False, index=True)
    title = Column(Text, nullable=False)
    description = Column(Text)
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    creation_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    image_url = Column(Text)
    icon_url = Column(Text)
    active = Column(Boolean, default=False, index=True)
    closed = Column(Boolean, default=False, index=True)
    archived = Column(Boolean, default=False)
    is_new = Column(Boolean, default=False)
    featured = Column(Boolean, default=False)
    restricted = Column(Boolean, default=False)
    liquidity = Column(Numeric)
    volume = Column(Numeric)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False)
    competitive = Column(Numeric)
    enable_order_book = Column(Boolean, default=False)
    neg_risk = Column(Boolean, default=False)
    neg_risk_market_id = Column(String)
    comment_count = Column(Numeric, default=0)
    
    # Relationships
    markets = relationship('Market', back_populates='event', cascade="all, delete-orphan")

from sqlalchemy import (
    Column,
    String,
    Integer,
    Numeric,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from .base import Base

class Outcome(Base):
    __tablename__ = 'outcomes'
    
    clob_token_id = Column(String, primary_key=True, nullable=False, index=True)
    market_id = Column(String, ForeignKey('markets.id'), nullable=False, index=True)
    name = Column(String, nullable=False)
    
    # Relationships
    market = relationship('Market', back_populates='outcomes')
    book_messages = relationship('BookMessage', back_populates='outcome', cascade="all, delete-orphan")
    price_change_messages = relationship('PriceChangeMessage', back_populates='outcome', cascade="all, delete-orphan")
    tick_size_change_messages = relationship('TickSizeChangeMessage', back_populates='outcome', cascade="all, delete-orphan")

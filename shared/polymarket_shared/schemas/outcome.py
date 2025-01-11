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
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    market_id = Column(String, ForeignKey('markets.id'), nullable=False, index=True)
    name = Column(String, nullable=False)
    clob_token_id = Column(String, nullable=False, unique=True, index=True)
    
    # Relationships
    market = relationship('Market', back_populates='outcomes')
    book_messages = relationship('BookMessage', back_populates='outcome', cascade="all, delete-orphan")
    price_change_messages = relationship('PriceChangeMessage', back_populates='outcome', cascade="all, delete-orphan")
    tick_size_change_messages = relationship('TickSizeChangeMessage', back_populates='outcome', cascade="all, delete-orphan")

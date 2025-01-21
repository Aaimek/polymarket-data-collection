from sqlalchemy import (
    Column,
    BigInteger,
    String,
    TIMESTAMP,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from .base import Base

class BookMessage(Base):
    __tablename__ = 'book_messages'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    # clob_token_id = Column(String, ForeignKey('outcomes.clob_token_id'), nullable=False, index=True)
    asset_id = Column(String, ForeignKey('outcomes.clob_token_id'), nullable=False, index=True)
    market = Column(String, nullable=False, index=True)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False, index=True)
    hash = Column(String)
    buys = Column(JSONB)
    sells = Column(JSONB)
    
    # Relationships
    outcome = relationship('Outcome', back_populates='book_messages')

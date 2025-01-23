from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Numeric,
    TIMESTAMP,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import JSONB
from .base import Base
from sqlalchemy.orm import relationship

class PriceChangeMessage(Base):
    __tablename__ = 'price_change_messages'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    # clob_token_id = Column(String, ForeignKey('outcomes.clob_token_id'), nullable=False, index=True)
    asset_id = Column(String, ForeignKey('outcomes.clob_token_id'), nullable=False, index=True)
    market = Column(String, nullable=False, index=True)
    changes = Column(JSONB)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False, index=True)
    hash = Column(String)
    
    # Relationships
    outcome = relationship('Outcome', back_populates='price_change_messages')

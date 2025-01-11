from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Numeric,
    TIMESTAMP,
    ForeignKey
)
from .base import Base
from sqlalchemy.orm import relationship

class PriceChangeMessage(Base):
    __tablename__ = 'price_change_messages'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    clob_token_id = Column(String, ForeignKey('outcomes.clob_token_id'), nullable=False, index=True)
    asset_id = Column(String, nullable=False)
    market = Column(String, nullable=False, index=True)
    price = Column(Numeric, nullable=False)
    size = Column(Numeric, nullable=False)
    side = Column(String, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False, index=True)
    hash = Column(String)
    
    # Relationships
    outcome = relationship('Outcome', back_populates='price_change_messages')

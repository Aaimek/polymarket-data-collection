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

class TickSizeChangeMessage(Base):
    __tablename__ = 'tick_size_change_messages'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    # clob_token_id = Column(String, ForeignKey('outcomes.clob_token_id'), nullable=False, index=True)
    asset_id = Column(String, ForeignKey('outcomes.clob_token_id'), nullable=False, index=True)
    market = Column(String, nullable=False, index=True)
    old_tick_size = Column(Numeric, nullable=False)
    new_tick_size = Column(Numeric, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False, index=True)
    
    # Relationships
    outcome = relationship('Outcome', back_populates='tick_size_change_messages')

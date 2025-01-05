from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Date,
    ForeignKey
)
from sqlalchemy.orm import relationship
from .base import Base

class ClobReward(Base):
    __tablename__ = 'clob_rewards'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    market_id = Column(String, ForeignKey('markets.id'), nullable=False, index=True)
    condition_id = Column(String, nullable=False)
    asset_address = Column(String, nullable=False)
    rewards_amount = Column(Numeric, default=0)
    rewards_daily_rate = Column(Numeric)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    # Relationships
    market = relationship('Market', back_populates='clob_rewards')

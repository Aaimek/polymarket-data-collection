from sqlalchemy import (
    Column,
    String,
    Text,
    Boolean,
    Numeric,
    TIMESTAMP,
    ForeignKey,
    Date
)
from sqlalchemy.orm import relationship
from .base import Base

class Market(Base):
    __tablename__ = 'markets'
    
    id = Column(String, primary_key=True)
    event_id = Column(String, ForeignKey('events.id'), nullable=False, index=True)
    question = Column(Text, nullable=False)
    condition_id = Column(String, nullable=False, index=True)
    slug = Column(String, nullable=False, index=True)
    resolution_source = Column(Text)
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    image_url = Column(Text)
    icon_url = Column(Text)
    description = Column(Text)
    volume = Column(Numeric)
    active = Column(Boolean, default=False, index=True)
    closed = Column(Boolean, default=False, index=True)
    market_maker_address = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False)
    closed_time = Column(TIMESTAMP(timezone=True))
    is_new = Column(Boolean, default=False)
    featured = Column(Boolean, default=False)
    submitted_by = Column(String)
    archived = Column(Boolean, default=False)
    resolved_by = Column(String)
    restricted = Column(Boolean, default=False)
    group_item_title = Column(String)
    group_item_threshold = Column(Numeric, default=0)
    question_id = Column(String)
    uma_end_date = Column(TIMESTAMP(timezone=True))
    enable_order_book = Column(Boolean, default=False)
    order_price_min_tick_size = Column(Numeric)
    order_min_size = Column(Numeric)
    uma_resolution_status = Column(String)
    volume_num = Column(Numeric)
    end_date_iso = Column(Date)
    start_date_iso = Column(Date)
    has_reviewed_dates = Column(Boolean, default=False)
    uma_bond = Column(Numeric)
    uma_reward = Column(Numeric)
    fpmm_live = Column(Boolean, default=False)
    volume_clob = Column(Numeric)
    accepting_orders = Column(Boolean, default=False)
    neg_risk = Column(Boolean, default=False)
    neg_risk_market_id = Column(String)
    neg_risk_request_id = Column(String)
    ready = Column(Boolean, default=False)
    funded = Column(Boolean, default=False)
    cyom = Column(Boolean, default=False)
    pager_duty_notification_enabled = Column(Boolean, default=False)
    approved = Column(Boolean, default=False)
    
    # Relationships
    event = relationship('Event', back_populates='markets')
    outcomes = relationship('Outcome', back_populates='market', cascade="all, delete-orphan")
    clob_rewards = relationship('ClobReward', back_populates='market', cascade="all, delete-orphan")

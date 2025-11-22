from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    event_type = Column(String) # sent, open, click, reply
    campaign_id = Column(String)
    lead_id = Column(String)
    details = Column(String, nullable=True)

class CampaignMetrics(Base):
    __tablename__ = 'campaign_metrics'
    
    id = Column(Integer, primary_key=True)
    campaign_id = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    sent_count = Column(Integer, default=0)
    open_count = Column(Integer, default=0)
    click_count = Column(Integer, default=0)
    reply_count = Column(Integer, default=0)
    open_rate = Column(Float, default=0.0)
    click_rate = Column(Float, default=0.0)
    reply_rate = Column(Float, default=0.0)

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(String, unique=True, index=True)
    content = Column(Text)
    media_type = Column(String)  # TEXT, IMAGE, VIDEO, CAROUSEL
    created_at = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    # Metrics
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    replies = Column(Integer, default=0)
    reposts = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    
    # Calculated fields
    engagement_rate = Column(Float, default=0.0)
    
    # Analysis
    analysis_result = Column(Text, nullable=True)
    analysis_date = Column(DateTime, nullable=True)
    analysis_cached = Column(Boolean, default=False)

class Analytics(Base):
    __tablename__ = "analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    total_posts = Column(Integer)
    avg_engagement_rate = Column(Float)
    best_post_id = Column(String)
    worst_post_id = Column(String)
    total_views = Column(Integer)
    total_likes = Column(Integer)
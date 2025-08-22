import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Post, Analytics


class TestModels:
    
    @pytest.fixture(scope="function")
    def db_session(self):
        # Create in-memory SQLite database for testing
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
        session.close()
    
    def test_post_model_creation(self, db_session):
        post = Post(
            thread_id="test_123",
            content="Test post content",
            media_type="TEXT",
            created_at=datetime.utcnow(),
            views=1000,
            likes=50,
            replies=10,
            reposts=5,
            shares=3,
            engagement_rate=6.8
        )
        
        db_session.add(post)
        db_session.commit()
        
        retrieved_post = db_session.query(Post).filter(Post.thread_id == "test_123").first()
        
        assert retrieved_post is not None
        assert retrieved_post.thread_id == "test_123"
        assert retrieved_post.content == "Test post content"
        assert retrieved_post.media_type == "TEXT"
        assert retrieved_post.views == 1000
        assert retrieved_post.engagement_rate == 6.8
    
    def test_post_model_defaults(self, db_session):
        post = Post(
            thread_id="test_456",
            content="Minimal post"
        )
        
        db_session.add(post)
        db_session.commit()
        
        retrieved_post = db_session.query(Post).filter(Post.thread_id == "test_456").first()
        
        assert retrieved_post.views == 0
        assert retrieved_post.likes == 0
        assert retrieved_post.replies == 0
        assert retrieved_post.reposts == 0
        assert retrieved_post.shares == 0
        assert retrieved_post.engagement_rate == 0.0
        assert retrieved_post.analysis_result is None
        assert retrieved_post.analysis_cached is False
    
    def test_post_model_unique_thread_id(self, db_session):
        post1 = Post(thread_id="duplicate_id", content="First post")
        post2 = Post(thread_id="duplicate_id", content="Second post")
        
        db_session.add(post1)
        db_session.commit()
        
        db_session.add(post2)
        
        # Should raise integrity error due to unique constraint
        with pytest.raises(Exception):
            db_session.commit()
    
    def test_analytics_model_creation(self, db_session):
        analytics = Analytics(
            total_posts=10,
            avg_engagement_rate=5.5,
            best_post_id="best_123",
            worst_post_id="worst_456",
            total_views=10000,
            total_likes=500
        )
        
        db_session.add(analytics)
        db_session.commit()
        
        retrieved_analytics = db_session.query(Analytics).first()
        
        assert retrieved_analytics is not None
        assert retrieved_analytics.total_posts == 10
        assert retrieved_analytics.avg_engagement_rate == 5.5
        assert retrieved_analytics.best_post_id == "best_123"
        assert retrieved_analytics.worst_post_id == "worst_456"
        assert retrieved_analytics.total_views == 10000
        assert retrieved_analytics.total_likes == 500
        assert retrieved_analytics.date is not None
    
    def test_post_model_analysis_fields(self, db_session):
        post = Post(
            thread_id="analysis_test",
            content="Post for analysis testing",
            analysis_result="This is AI analysis result",
            analysis_date=datetime.utcnow(),
            analysis_cached=True
        )
        
        db_session.add(post)
        db_session.commit()
        
        retrieved_post = db_session.query(Post).filter(Post.thread_id == "analysis_test").first()
        
        assert retrieved_post.analysis_result == "This is AI analysis result"
        assert retrieved_post.analysis_date is not None
        assert retrieved_post.analysis_cached is True
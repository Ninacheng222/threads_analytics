import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from analytics import ContentAnalyzer, MetricsCalculator
from models import Post


class TestContentAnalyzer:
    
    @pytest.fixture
    def analyzer(self):
        return ContentAnalyzer()
    
    @pytest.fixture
    def sample_post(self):
        return Post(
            thread_id="test_123",
            content="This is a test post about AI technology",
            views=1000,
            likes=50,
            engagement_rate=5.0,
            analysis_result=None,
            analysis_date=None
        )
    
    @pytest.mark.asyncio
    async def test_analyze_post_content_new_analysis(self, analyzer, sample_post, mock_openai_response):
        with patch('openai.ChatCompletion.acreate') as mock_openai:
            mock_openai.return_value = mock_openai_response
            
            result = await analyzer.analyze_post_content(sample_post)
            
            assert "Educational" in result
            assert "performed well" in result
            assert sample_post.analysis_result == result
            assert sample_post.analysis_date is not None
            assert sample_post.analysis_cached is True
            mock_openai.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_analyze_post_content_cached(self, analyzer, sample_post):
        # Set up cached analysis
        sample_post.analysis_result = "Cached analysis result"
        sample_post.analysis_date = datetime.utcnow()
        sample_post.analysis_cached = True
        
        with patch('openai.ChatCompletion.acreate') as mock_openai:
            result = await analyzer.analyze_post_content(sample_post)
            
            assert result == "Cached analysis result"
            mock_openai.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_analyze_post_content_expired_cache(self, analyzer, sample_post, mock_openai_response):
        # Set up expired cache (older than cache_days)
        sample_post.analysis_result = "Old analysis"
        sample_post.analysis_date = datetime.utcnow() - timedelta(days=35)
        
        with patch('openai.ChatCompletion.acreate') as mock_openai:
            mock_openai.return_value = mock_openai_response
            
            result = await analyzer.analyze_post_content(sample_post)
            
            assert "Educational" in result
            mock_openai.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_analyze_post_content_api_error(self, analyzer, sample_post):
        with patch('openai.ChatCompletion.acreate') as mock_openai:
            mock_openai.side_effect = Exception("API Error")
            
            result = await analyzer.analyze_post_content(sample_post)
            
            assert "Analysis unavailable" in result
            assert "API Error" in result
    
    def test_is_analysis_cached_no_analysis(self, analyzer, sample_post):
        result = analyzer._is_analysis_cached(sample_post)
        assert result is False
    
    def test_is_analysis_cached_recent(self, analyzer, sample_post):
        sample_post.analysis_result = "Test analysis"
        sample_post.analysis_date = datetime.utcnow()
        
        result = analyzer._is_analysis_cached(sample_post)
        assert result is True
    
    def test_is_analysis_cached_expired(self, analyzer, sample_post):
        sample_post.analysis_result = "Test analysis"
        sample_post.analysis_date = datetime.utcnow() - timedelta(days=35)
        
        result = analyzer._is_analysis_cached(sample_post)
        assert result is False


class TestMetricsCalculator:
    
    @pytest.fixture
    def mock_db(self):
        return MagicMock(spec=Session)
    
    @pytest.fixture
    def sample_posts(self):
        return [
            Post(
                thread_id="post_1",
                content="High performing post",
                views=2000,
                likes=100,
                engagement_rate=8.0
            ),
            Post(
                thread_id="post_2", 
                content="Medium performing post",
                views=1000,
                likes=30,
                engagement_rate=3.0
            ),
            Post(
                thread_id="post_3",
                content="Low performing post", 
                views=500,
                likes=5,
                engagement_rate=1.0
            )
        ]
    
    def test_calculate_summary_stats_with_posts(self, mock_db, sample_posts):
        mock_db.query().all.return_value = sample_posts
        
        result = MetricsCalculator.calculate_summary_stats(mock_db)
        
        assert result["total_posts"] == 3
        assert result["avg_engagement"] == 4.0  # (8.0 + 3.0 + 1.0) / 3
        assert result["total_views"] == 3500  # 2000 + 1000 + 500
        assert result["total_likes"] == 135   # 100 + 30 + 5
        assert result["best_post"]["engagement_rate"] == 8.0
        assert result["worst_post"]["engagement_rate"] == 1.0
        assert "High performing" in result["best_post"]["content"]
        assert "Low performing" in result["worst_post"]["content"]
    
    def test_calculate_summary_stats_no_posts(self, mock_db):
        mock_db.query().all.return_value = []
        
        result = MetricsCalculator.calculate_summary_stats(mock_db)
        
        assert result["total_posts"] == 0
        assert result["avg_engagement"] == 0
        assert result["best_post"] is None
        assert result["worst_post"] is None
    
    def test_calculate_summary_stats_single_post(self, mock_db):
        single_post = [Post(
            thread_id="post_1",
            content="Only post",
            views=1000,
            likes=50,
            engagement_rate=5.0
        )]
        mock_db.query().all.return_value = single_post
        
        result = MetricsCalculator.calculate_summary_stats(mock_db)
        
        assert result["total_posts"] == 1
        assert result["avg_engagement"] == 5.0
        assert result["best_post"]["engagement_rate"] == 5.0
        assert result["worst_post"]["engagement_rate"] == 5.0
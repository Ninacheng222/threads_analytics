import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from datetime import datetime

from models import Post


class TestAPIEndpoints:
    
    def test_dashboard_endpoint(self, client):
        """Test main dashboard page loads"""
        response = client.get("/")
        
        assert response.status_code == 200
        assert "Threads Analytics Dashboard" in response.text
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    def test_get_posts_empty_database(self, client, test_db):
        """Test getting posts when database is empty"""
        response = client.get("/api/posts")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_posts_with_data(self, client, test_db):
        """Test getting posts with sample data"""
        # Add test post to database
        test_post = Post(
            thread_id="test_123",
            content="Test post content",
            media_type="TEXT",
            created_at=datetime.utcnow(),
            views=1000,
            likes=50,
            engagement_rate=5.0
        )
        test_db.add(test_post)
        test_db.commit()
        
        response = client.get("/api/posts")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["thread_id"] == "test_123"
        assert data[0]["content"] == "Test post content"
        assert data[0]["views"] == 1000
        assert data[0]["engagement_rate"] == 5.0
    
    def test_get_analytics_empty_database(self, client, test_db):
        """Test analytics endpoint with empty database"""
        response = client.get("/api/analytics")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_posts"] == 0
        assert data["avg_engagement"] == 0
    
    def test_get_analytics_with_data(self, client, test_db):
        """Test analytics endpoint with sample data"""
        # Add test posts
        posts = [
            Post(thread_id="post_1", content="Post 1", views=1000, likes=50, engagement_rate=5.0),
            Post(thread_id="post_2", content="Post 2", views=2000, likes=100, engagement_rate=5.0)
        ]
        
        for post in posts:
            test_db.add(post)
        test_db.commit()
        
        response = client.get("/api/analytics")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_posts"] == 2
        assert data["avg_engagement"] == 5.0
        assert data["total_views"] == 3000
        assert data["total_likes"] == 150
    
    @patch('data_collector.ThreadsAPIClient.get_user_media')
    @patch('data_collector.ThreadsAPIClient.get_media_insights')
    def test_sync_data_success(self, mock_insights, mock_media, client, test_db):
        """Test successful data sync from Threads API"""
        # Mock API responses
        mock_media.return_value = [{
            "id": "new_post_123",
            "text": "New post from API",
            "media_type": "TEXT",
            "timestamp": "2024-01-15T10:30:00Z"
        }]
        
        mock_insights.return_value = {
            "views": 500,
            "likes": 25,
            "replies": 5,
            "reposts": 2,
            "shares": 1
        }
        
        response = client.post("/api/sync")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "Synced 1 posts" in data["message"]
        
        # Verify post was created in database
        posts = client.get("/api/posts").json()
        assert len(posts) == 1
        assert posts[0]["thread_id"] == "new_post_123"
        assert posts[0]["views"] == 500
    
    @patch('data_collector.ThreadsAPIClient.get_user_media')
    def test_sync_data_api_error(self, mock_media, client, test_db):
        """Test sync data with API error"""
        mock_media.side_effect = Exception("API connection failed")
        
        response = client.post("/api/sync")
        
        assert response.status_code == 500
        assert "Sync failed" in response.json()["detail"]
    
    @patch('analytics.ContentAnalyzer.analyze_post_content')
    def test_analyze_posts_success(self, mock_analyze, client, test_db):
        """Test successful post analysis"""
        # Add test post
        test_post = Post(
            thread_id="analyze_me",
            content="Post to analyze",
            views=1000,
            likes=50,
            engagement_rate=5.0
        )
        test_db.add(test_post)
        test_db.commit()
        
        # Mock analysis result
        mock_analyze.return_value = "Great post about technology!"
        
        response = client.post("/api/analyze", json={"post_ids": ["analyze_me"]})
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["analyzed_count"] == 1
        
        # Verify analysis was saved
        posts = client.get("/api/posts").json()
        assert posts[0]["analysis_result"] == "Great post about technology!"
    
    def test_analyze_posts_no_ids(self, client, test_db):
        """Test analysis endpoint with no post IDs"""
        response = client.post("/api/analyze", json={"post_ids": []})
        
        assert response.status_code == 400
        assert "No post IDs provided" in response.json()["detail"]
    
    def test_analyze_posts_nonexistent_posts(self, client, test_db):
        """Test analysis with non-existent post IDs"""
        response = client.post("/api/analyze", json={"post_ids": ["nonexistent"]})
        
        assert response.status_code == 200
        data = response.json()
        assert data["analyzed_count"] == 0
    
    @patch('analytics.ContentAnalyzer.analyze_post_content')
    def test_analyze_posts_limit_enforcement(self, mock_analyze, client, test_db):
        """Test that analysis respects MAX_POSTS_PER_ANALYSIS limit"""
        # Add multiple test posts
        for i in range(15):
            post = Post(
                thread_id=f"post_{i}",
                content=f"Post {i} content",
                views=1000,
                likes=50,
                engagement_rate=5.0
            )
            test_db.add(post)
        test_db.commit()
        
        mock_analyze.return_value = "Analysis result"
        
        # Try to analyze 15 posts (limit is 10)
        post_ids = [f"post_{i}" for i in range(15)]
        response = client.post("/api/analyze", json={"post_ids": post_ids})
        
        assert response.status_code == 200
        data = response.json()
        
        # Should only analyze up to the limit (10 posts)
        assert data["analyzed_count"] == 10
        assert mock_analyze.call_count == 10


class TestAPIErrorHandling:
    
    def test_invalid_endpoint(self, client):
        """Test 404 for invalid endpoint"""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
    
    def test_invalid_method(self, client):
        """Test 405 for invalid HTTP method"""
        response = client.delete("/api/posts")
        assert response.status_code == 405
    
    def test_invalid_json(self, client):
        """Test 422 for invalid JSON in request body"""
        response = client.post("/api/analyze", data="invalid json")
        assert response.status_code == 422
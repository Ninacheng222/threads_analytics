import pytest
from unittest.mock import AsyncMock, patch
import httpx

from data_collector import ThreadsAPIClient


class TestThreadsAPIClient:
    
    @pytest.fixture
    def client(self):
        return ThreadsAPIClient()
    
    @pytest.mark.asyncio
    async def test_get_user_media_success(self, client, sample_post_data):
        mock_response = {
            "data": [sample_post_data]
        }
        
        with patch('httpx.AsyncClient.get') as mock_get:
            mock_get.return_value.json.return_value = mock_response
            mock_get.return_value.raise_for_status.return_value = None
            
            result = await client.get_user_media(limit=1)
            
            assert len(result) == 1
            assert result[0]["id"] == "test_post_123"
            assert result[0]["text"] == "This is a test post about technology trends"
            mock_get.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_user_media_api_error(self, client):
        with patch('httpx.AsyncClient.get') as mock_get:
            mock_get.return_value.raise_for_status.side_effect = httpx.HTTPStatusError(
                "API Error", request=None, response=None
            )
            
            with pytest.raises(httpx.HTTPStatusError):
                await client.get_user_media()
    
    @pytest.mark.asyncio
    async def test_get_media_insights_success(self, client, sample_insights_data):
        mock_response = {
            "data": [
                {"name": "views", "values": [{"value": 1000}]},
                {"name": "likes", "values": [{"value": 50}]},
                {"name": "replies", "values": [{"value": 10}]},
                {"name": "reposts", "values": [{"value": 5}]},
                {"name": "shares", "values": [{"value": 3}]}
            ]
        }
        
        with patch('httpx.AsyncClient.get') as mock_get:
            mock_get.return_value.json.return_value = mock_response
            mock_get.return_value.raise_for_status.return_value = None
            
            result = await client.get_media_insights("test_post_123")
            
            assert result["views"] == 1000
            assert result["likes"] == 50
            assert result["replies"] == 10
            assert result["reposts"] == 5
            assert result["shares"] == 3
    
    def test_calculate_engagement_rate_normal(self, client):
        metrics = {
            "views": 1000,
            "likes": 50,
            "replies": 10,
            "reposts": 5,
            "shares": 3
        }
        
        engagement_rate = client.calculate_engagement_rate(metrics)
        
        # (50 + 10 + 5 + 3) / 1000 * 100 = 6.8%
        assert engagement_rate == 6.8
    
    def test_calculate_engagement_rate_zero_views(self, client):
        metrics = {
            "views": 0,
            "likes": 50,
            "replies": 10,
            "reposts": 5,
            "shares": 3
        }
        
        engagement_rate = client.calculate_engagement_rate(metrics)
        
        assert engagement_rate == 0.0
    
    def test_calculate_engagement_rate_missing_metrics(self, client):
        metrics = {
            "views": 1000,
            "likes": 50
            # Missing replies, reposts, shares
        }
        
        engagement_rate = client.calculate_engagement_rate(metrics)
        
        # Only likes counted: 50 / 1000 * 100 = 5%
        assert engagement_rate == 5.0
import httpx
from datetime import datetime
from typing import List, Dict, Optional
from config import settings

class ThreadsAPIClient:
    def __init__(self):
        self.base_url = "https://graph.threads.net"
        self.access_token = settings.THREADS_ACCESS_TOKEN
        self.user_id = settings.THREADS_USER_ID
    
    async def get_user_media(self, limit: int = 25) -> List[Dict]:
        """Fetch user's posts/media"""
        url = f"{self.base_url}/{self.user_id}/threads"
        params = {
            "fields": "id,media_type,media_url,permalink,username,text,timestamp,is_quote_post",
            "limit": limit,
            "access_token": self.access_token
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json().get("data", [])
    
    async def get_media_insights(self, media_id: str) -> Dict:
        """Fetch insights/metrics for a specific post"""
        url = f"{self.base_url}/{media_id}/insights"
        params = {
            "metric": "views,likes,replies,reposts,shares",
            "access_token": self.access_token
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json().get("data", [])
            
            # Convert insights array to dict
            insights = {}
            for item in data:
                insights[item["name"]] = item["values"][0]["value"]
            
            return insights
    
    def calculate_engagement_rate(self, metrics: Dict) -> float:
        """Calculate engagement rate: (likes + replies + reposts + shares) / views * 100"""
        views = metrics.get("views", 0)
        if views == 0:
            return 0.0
        
        engagement = (
            metrics.get("likes", 0) +
            metrics.get("replies", 0) +
            metrics.get("reposts", 0) +
            metrics.get("shares", 0)
        )
        
        return round((engagement / views) * 100, 2)
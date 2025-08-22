import openai
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from models import Post, Analytics
from config import settings

openai.api_key = settings.OPENAI_API_KEY

class ContentAnalyzer:
    def __init__(self):
        self.max_posts = settings.MAX_POSTS_PER_ANALYSIS
        self.cache_days = settings.CACHE_ANALYSIS_DAYS
    
    async def analyze_post_content(self, post: Post) -> str:
        """Analyze a single post using OpenAI"""
        if self._is_analysis_cached(post):
            return post.analysis_result
        
        prompt = f"""
        Analyze this Threads post performance:
        
        Content: "{post.content[:500]}..."
        Metrics: {post.likes} likes, {post.views} views, {post.engagement_rate}% engagement
        
        Provide analysis covering:
        1. Content type (educational/entertainment/personal/promotional)
        2. Why it performed well/poorly (be specific)
        3. One actionable improvement suggestion
        
        Keep response under 100 words, be direct and helpful.
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.7
            )
            
            analysis = response.choices[0].message.content.strip()
            self._cache_analysis(post, analysis)
            return analysis
            
        except Exception as e:
            return f"Analysis unavailable: {str(e)}"
    
    def _is_analysis_cached(self, post: Post) -> bool:
        """Check if analysis is recent enough to use cache"""
        if not post.analysis_result or not post.analysis_date:
            return False
        
        cache_expiry = datetime.utcnow() - timedelta(days=self.cache_days)
        return post.analysis_date > cache_expiry
    
    def _cache_analysis(self, post: Post, analysis: str):
        """Update post with analysis results"""
        post.analysis_result = analysis
        post.analysis_date = datetime.utcnow()
        post.analysis_cached = True

class MetricsCalculator:
    @staticmethod
    def calculate_summary_stats(db: Session) -> Dict:
        """Calculate overall analytics summary"""
        posts = db.query(Post).all()
        
        if not posts:
            return {"total_posts": 0, "avg_engagement": 0, "best_post": None, "worst_post": None}
        
        total_posts = len(posts)
        avg_engagement = sum(p.engagement_rate for p in posts) / total_posts
        best_post = max(posts, key=lambda p: p.engagement_rate)
        worst_post = min(posts, key=lambda p: p.engagement_rate)
        
        return {
            "total_posts": total_posts,
            "avg_engagement": round(avg_engagement, 2),
            "total_views": sum(p.views for p in posts),
            "total_likes": sum(p.likes for p in posts),
            "best_post": {
                "id": best_post.thread_id,
                "content": best_post.content[:100] + "...",
                "engagement_rate": best_post.engagement_rate
            },
            "worst_post": {
                "id": worst_post.thread_id,
                "content": worst_post.content[:100] + "...", 
                "engagement_rate": worst_post.engagement_rate
            }
        }
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
        self.creator_archetypes = [
            "The Authentic Storyteller", "The Trendsetter", "The Community Builder",
            "The Knowledge Sharer", "The Conversation Starter", "The Visual Artist",
            "The Behind-the-Scenes Creator", "The Motivational Voice"
        ]
    
    async def generate_creator_portrait(self, posts: List[Post]) -> Dict:
        """Generate mystical creator personality analysis"""
        if not posts:
            return self._default_portrait()
        
        # Analyze content patterns
        content_analysis = self._analyze_content_patterns(posts)
        engagement_patterns = self._analyze_engagement_patterns(posts)
        
        prompt = f"""
        🔮 You are a mystical digital fortune teller analyzing a content creator's aura.
        
        Creator's Digital Energy:
        - Total posts analyzed: {len(posts)}
        - Content themes: {content_analysis['themes']}
        - Posting patterns: {content_analysis['patterns']}
        - Engagement aura: {engagement_patterns}
        - Average engagement rate: {sum(p.engagement_rate for p in posts) / len(posts):.1f}%
        
        Channel the universe and create a mystical "Creator Portrait" with:
        
        1. ARCHETYPE: Choose from {self.creator_archetypes} (pick the most fitting)
        2. CONTENT DNA: Breakdown as percentages (Personal: X%, Educational: Y%, Entertainment: Z%)
        3. POSTING SPIRIT: Describe their posting personality (Night Owl, Consistent Creator, etc.)
        4. ENGAGEMENT INSIGHT: What their audience loves about them (be specific and encouraging)
        5. CREATOR LEVEL: Give them a mystical level name with encouraging message
        6. MYSTICAL ADVICE: One piece of cosmic creator wisdom
        
        Response format (JSON):
        {{
            "archetype": "The [Archetype Name]",
            "content_dna": {{"personal": 40, "educational": 30, "entertainment": 30}},
            "posting_spirit": "Night Owl Creator",
            "engagement_insight": "Your audience craves your authentic vulnerability",
            "creator_level": "Rising Star ⭐",
            "mystical_advice": "The universe rewards consistency over perfection",
            "shareable_quote": "✨ Your content resonates with the frequency of authenticity ✨"
        }}
        
        Write in mystical, engaging language that people want to share. Be positive and encouraging.
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.8
            )
            
            import json
            result = json.loads(response.choices[0].message.content.strip())
            result['total_posts'] = len(posts)
            result['avg_engagement'] = round(sum(p.engagement_rate for p in posts) / len(posts), 1)
            return result
            
        except Exception as e:
            return self._default_portrait()
    
    async def analyze_post_content(self, post: Post) -> str:
        """Analyze a single post using OpenAI (legacy method)"""
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
    
    def _analyze_content_patterns(self, posts: List[Post]) -> Dict:
        """Analyze posting patterns and themes"""
        themes = []
        patterns = {}
        
        # Analyze content themes based on keywords
        for post in posts:
            content = post.content.lower()
            if any(word in content for word in ['personal', 'life', 'feel', 'think']):
                themes.append('personal')
            elif any(word in content for word in ['tip', 'how', 'learn', 'guide']):
                themes.append('educational')
            elif any(word in content for word in ['funny', 'lol', 'haha', 'joke']):
                themes.append('entertainment')
            else:
                themes.append('general')
        
        # Calculate theme distribution
        theme_counts = {theme: themes.count(theme) for theme in set(themes)}
        total = len(themes)
        theme_percentages = {theme: round((count/total)*100) for theme, count in theme_counts.items()}
        
        return {
            'themes': theme_percentages,
            'patterns': f"{len(posts)} posts analyzed"
        }
    
    def _analyze_engagement_patterns(self, posts: List[Post]) -> str:
        """Analyze what content performs best"""
        if not posts:
            return "Mysterious energy patterns"
        
        best_post = max(posts, key=lambda p: p.engagement_rate)
        avg_engagement = sum(p.engagement_rate for p in posts) / len(posts)
        
        if avg_engagement > 5:
            return "High-vibrational content that deeply resonates"
        elif avg_engagement > 2:
            return "Steady creative energy with growing influence"
        else:
            return "Emerging digital aura with untapped potential"
    
    def _default_portrait(self) -> Dict:
        """Default portrait for new creators or errors"""
        return {
            "archetype": "The Emerging Creator",
            "content_dna": {"personal": 50, "educational": 25, "entertainment": 25},
            "posting_spirit": "Digital Wanderer",
            "engagement_insight": "Your unique voice is waiting to be discovered",
            "creator_level": "Cosmic Beginner 🌟",
            "mystical_advice": "Every creator's journey begins with a single post",
            "shareable_quote": "✨ Your creative energy is just beginning to shine ✨",
            "total_posts": 0,
            "avg_engagement": 0
        }
    
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
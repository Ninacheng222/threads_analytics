from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from database import get_db, create_tables
from models import Post, Analytics
from data_collector import ThreadsAPIClient
from analytics import ContentAnalyzer, MetricsCalculator
from content_generator import ShareableContentGenerator
from config import settings

# Initialize FastAPI app
app = FastAPI(title="Threads Fortune Teller", version="1.0.0")

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize services
threads_client = ThreadsAPIClient()
content_analyzer = ContentAnalyzer()
metrics_calculator = MetricsCalculator()
content_generator = ShareableContentGenerator()

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

@app.get("/", response_class=HTMLResponse)
async def fortune_teller_home(request: Request):
    """Threads Fortune Teller home page"""
    return templates.TemplateResponse("fortune_teller.html", {"request": request})

@app.get("/api/posts")
async def get_posts(db: Session = Depends(get_db)):
    """Get all posts with metrics"""
    posts = db.query(Post).all()
    return [
        {
            "thread_id": post.thread_id,
            "content": post.content,
            "media_type": post.media_type,
            "created_at": post.created_at.isoformat() if post.created_at else None,
            "views": post.views,
            "likes": post.likes,
            "replies": post.replies,
            "reposts": post.reposts,
            "shares": post.shares,
            "engagement_rate": post.engagement_rate,
            "analysis_result": post.analysis_result,
            "analysis_cached": post.analysis_cached
        }
        for post in posts
    ]

@app.get("/api/analytics")
async def get_analytics(db: Session = Depends(get_db)):
    """Get summary analytics"""
    return metrics_calculator.calculate_summary_stats(db)

@app.post("/api/sync")
async def sync_data(db: Session = Depends(get_db)):
    """Sync data from Threads API"""
    try:
        # Fetch posts from Threads API
        media_data = await threads_client.get_user_media(limit=50)
        
        for media in media_data:
            # Check if post already exists
            existing_post = db.query(Post).filter(Post.thread_id == media["id"]).first()
            
            if existing_post:
                # Update existing post metrics
                insights = await threads_client.get_media_insights(media["id"])
                existing_post.views = insights.get("views", 0)
                existing_post.likes = insights.get("likes", 0)
                existing_post.replies = insights.get("replies", 0)
                existing_post.reposts = insights.get("reposts", 0)
                existing_post.shares = insights.get("shares", 0)
                existing_post.engagement_rate = threads_client.calculate_engagement_rate(insights)
                existing_post.updated_at = datetime.utcnow()
            else:
                # Create new post
                insights = await threads_client.get_media_insights(media["id"])
                
                new_post = Post(
                    thread_id=media["id"],
                    content=media.get("text", ""),
                    media_type=media.get("media_type", "TEXT"),
                    created_at=datetime.fromisoformat(media["timestamp"].replace("Z", "+00:00")),
                    views=insights.get("views", 0),
                    likes=insights.get("likes", 0),
                    replies=insights.get("replies", 0),
                    reposts=insights.get("reposts", 0),
                    shares=insights.get("shares", 0),
                    engagement_rate=threads_client.calculate_engagement_rate(insights)
                )
                
                db.add(new_post)
        
        db.commit()
        return {"status": "success", "message": f"Synced {len(media_data)} posts"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")

@app.post("/api/analyze")
async def analyze_posts(
    request: dict,  # {"post_ids": ["id1", "id2", ...]}
    db: Session = Depends(get_db)
):
    """Analyze selected posts with LLM"""
    post_ids = request.get("post_ids", [])
    
    if not post_ids:
        raise HTTPException(status_code=400, detail="No post IDs provided")
    
    # Limit analysis to prevent high costs
    if len(post_ids) > settings.MAX_POSTS_PER_ANALYSIS:
        post_ids = post_ids[:settings.MAX_POSTS_PER_ANALYSIS]
    
    try:
        analyzed_count = 0
        
        for post_id in post_ids:
            post = db.query(Post).filter(Post.thread_id == post_id).first()
            if post:
                analysis = await content_analyzer.analyze_post_content(post)
                post.analysis_result = analysis
                post.analysis_date = datetime.utcnow()
                analyzed_count += 1
        
        db.commit()
        return {
            "status": "success", 
            "message": f"Analyzed {analyzed_count} posts",
            "analyzed_count": analyzed_count
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/generate-portrait")
async def generate_creator_portrait(db: Session = Depends(get_db)):
    """Generate mystical creator portrait"""
    try:
        posts = db.query(Post).all()
        
        if not posts:
            raise HTTPException(status_code=400, detail="No posts found. Please sync data first.")
        
        # Generate the creator portrait
        portrait = await content_analyzer.generate_creator_portrait(posts)
        
        # Generate shareable content
        ig_story_image = content_generator.generate_ig_story_image(portrait)
        share_urls = content_generator.generate_share_urls(portrait)
        
        return {
            "status": "success",
            "portrait": portrait,
            "shareable_content": {
                "ig_story_image": ig_story_image,
                "share_urls": share_urls
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Portrait generation failed: {str(e)}")

@app.get("/api/share-content/{portrait_id}")
async def get_shareable_content(portrait_id: str):
    """Get pre-generated shareable content"""
    # In a real app, you'd store portraits and retrieve by ID
    # For MVP, we'll return a sample
    return {
        "threads_text": "🔮 Just discovered my Creator DNA! ✨ Your content resonates with the frequency of authenticity ✨",
        "ig_story_url": "/static/sample-story.png"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
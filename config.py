import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Threads API
    THREADS_ACCESS_TOKEN = os.getenv("THREADS_ACCESS_TOKEN", "")
    THREADS_USER_ID = os.getenv("THREADS_USER_ID", "")
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")
    
    # Analysis limits (cost control)
    MAX_POSTS_PER_ANALYSIS = 10
    CACHE_ANALYSIS_DAYS = 30

settings = Settings()
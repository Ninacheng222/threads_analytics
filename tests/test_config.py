import pytest
import os
from unittest.mock import patch

from config import Settings


class TestConfig:
    
    def test_settings_default_values(self):
        """Test default configuration values"""
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings()
            
            assert settings.THREADS_ACCESS_TOKEN == ""
            assert settings.THREADS_USER_ID == ""
            assert settings.OPENAI_API_KEY == ""
            assert settings.DATABASE_URL == "sqlite:///./data.db"
            assert settings.MAX_POSTS_PER_ANALYSIS == 10
            assert settings.CACHE_ANALYSIS_DAYS == 30
    
    def test_settings_from_environment(self):
        """Test configuration from environment variables"""
        test_env = {
            "THREADS_ACCESS_TOKEN": "test_token_123",
            "THREADS_USER_ID": "test_user_456",
            "OPENAI_API_KEY": "test_openai_key",
            "DATABASE_URL": "postgresql://test:test@localhost/test"
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            
            assert settings.THREADS_ACCESS_TOKEN == "test_token_123"
            assert settings.THREADS_USER_ID == "test_user_456"
            assert settings.OPENAI_API_KEY == "test_openai_key"
            assert settings.DATABASE_URL == "postgresql://test:test@localhost/test"
    
    def test_settings_partial_environment(self):
        """Test configuration with some env vars set"""
        test_env = {
            "THREADS_ACCESS_TOKEN": "partial_token",
            "OPENAI_API_KEY": "partial_openai_key"
        }
        
        with patch.dict(os.environ, test_env, clear=True):
            settings = Settings()
            
            assert settings.THREADS_ACCESS_TOKEN == "partial_token"
            assert settings.THREADS_USER_ID == ""  # Still default
            assert settings.OPENAI_API_KEY == "partial_openai_key"
            assert settings.DATABASE_URL == "sqlite:///./data.db"  # Still default
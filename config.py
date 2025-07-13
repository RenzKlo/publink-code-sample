import os
import json
from datetime import timedelta


class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # MongoDB Configuration
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/publink_users'
    
    # Google OAuth Configuration
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID') or '449146938143-u2p4aqi52i2vmgh198ko9hsvqeanterp.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    
    # Security Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # CORS Configuration
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000').split(',')
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL', 'memory://')
    
    # Timezone
    TIMEZONE = 'Asia/Manila'
    
    # Token expiration
    TOKEN_EXPIRATION_HOURS = 24
    
    # Security Headers
    SECURITY_HEADERS = {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Content-Security-Policy': "default-src 'self'"
    }


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/publink_users'


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback-secret-key-change-in-production'
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/publink_users'
    
    def __init__(self):
        # Validate required environment variables for production
        if self.SECRET_KEY == 'fallback-secret-key-change-in-production':
            print("Warning: Using fallback SECRET_KEY. Set SECRET_KEY environment variable for production.")
        if not os.environ.get('MONGO_URI'):
            print("Warning: Using default MONGO_URI. Set MONGO_URI environment variable for production.")


class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    MONGO_URI = 'mongodb://localhost:27017/publink_test'


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Legacy support for existing code
google_client_id = Config.GOOGLE_CLIENT_ID
MONGODB_URL2 = 'mongodb://localhost:27017'  # Base MongoDB URL for legacy support
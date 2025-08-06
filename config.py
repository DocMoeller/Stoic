import os
from pathlib import Path

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Storage configuration
    BASE_DIR = Path(__file__).parent
    STORAGE_DIR = BASE_DIR / 'storage'
    REFLECTIONS_FILE = STORAGE_DIR / 'reflections.json'
    
    # Application settings
    DEBUG = True
    
    @classmethod
    def init_app(cls, app):
        """Initialize the Flask app with configuration."""
        # Ensure storage directory exists
        cls.STORAGE_DIR.mkdir(exist_ok=True)

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback-secret-key'

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    REFLECTIONS_FILE = Config.BASE_DIR / 'storage' / 'test_reflections.json'

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

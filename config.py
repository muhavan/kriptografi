import os
from pathlib import Path

# Load .env file if available
try:
    from dotenv import load_dotenv
    BASE_DIR = Path(__file__).resolve().parent
    load_dotenv(BASE_DIR / '.env')
except ImportError:
    BASE_DIR = Path(__file__).resolve().parent

class Config:
    """Base Configuration"""
    BASE_DIR = Path(__file__).resolve().parent
    
    # Secret Key for sessions and security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-kriptografi-insecure-dev-key-change-this-in-production')
    
    # Storage folders
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploaded_files')
    SIGNED_FOLDER = os.path.join(BASE_DIR, 'signed_files')
    
    # Upload limits
    MAX_UPLOAD_MB = int(os.environ.get('MAX_UPLOAD_MB', 16))
    MAX_CONTENT_LENGTH = MAX_UPLOAD_MB * 1024 * 1024  # default 16 MB
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {
        'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'txt',
        'py', 'html', 'php', 'json', 'js', 'css', 'xml', 'java',
        'c', 'cpp', 'cs', 'go', 'rb', 'ts', 'jsx', 'tsx', 'md',
        'yml', 'yaml', 'sql', 'sh', 'bat'
    }

class DevelopmentConfig(Config):
    """Development Configuration"""
    DEBUG = True
    TESTING = False
    ENV = 'development'

class ProductionConfig(Config):
    """Production Configuration"""
    DEBUG = False
    TESTING = False
    ENV = 'production'
    
    # In production, require or strongly suggest setting SECRET_KEY in .env
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    # Uncomment if using HTTPS:
    # SESSION_COOKIE_SECURE = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig if os.environ.get('FLASK_ENV') != 'production' else ProductionConfig
}

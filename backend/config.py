import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/webguard.db')
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_HOST = os.getenv('FLASK_HOST', '127.0.0.1')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
    
    # Monitoring
    DEFAULT_CHECK_INTERVAL = int(os.getenv('DEFAULT_CHECK_INTERVAL', 300))  # 5 minutes
    CHECK_TIMEOUT = int(os.getenv('CHECK_TIMEOUT', 30))  # 30 seconds
    MIN_CHECK_INTERVAL = 60  # 1 minute minimum
    
    # SSL Certificate Warnings (days before expiry)
    SSL_WARNING_THRESHOLDS = [30, 14, 7, 0]  # 30 days, 14 days, 7 days, expired
    
    # Notification
    NOTIFICATION_COOLDOWN = 300  # 5 minutes between duplicate notifications


import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-braincoach-ai'
    # Default to SQLite for easy local development, but can be overridden by env var for MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///braincoach.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Mail settings (for PDF reports)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

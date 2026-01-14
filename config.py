import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # ----------------------
    # Core Flask Settings
    # ----------------------
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-this")

    DEBUG = False
    TESTING = False

    # ----------------------
    # Database Configuration
    # ----------------------
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "telemedicine.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ----------------------
    # JWT Authentication
    # ----------------------
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-secret-change-this")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    # ----------------------
    # AI / ML Configuration
    # ----------------------
    AI_MODEL_TYPE = os.environ.get("AI_MODEL_TYPE", "rule_based")
    AI_CONFIDENCE_THRESHOLD = 0.6

    # Example for future LLM usage
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

    # ----------------------
    # Voice Processing
    # ----------------------
    SPEECH_LANGUAGE = "en-IN"   # Indian English
    AUDIO_UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads", "audio")
    MAX_AUDIO_SIZE_MB = 10

    # ----------------------
    # Offline Sync Settings
    # ----------------------
    SYNC_BATCH_SIZE = 100
    SYNC_TIME_WINDOW_MINUTES = 30

    # ----------------------
    # Medical Safety Settings
    # ----------------------
    EMERGENCY_KEYWORDS = [
        "chest pain",
        "breathing problem",
        "unconscious",
        "severe bleeding",
        "heart attack"
    ]

    # ----------------------
    # Rate Limiting (future)
    # ----------------------
    RATELIMIT_DEFAULT = "100/hour"

    # ----------------------
    # Logging
    # ----------------------
    LOG_LEVEL = "INFO"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

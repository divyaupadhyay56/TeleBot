import os
from dotenv import load_dotenv

# Load variables from .env into environment
load_dotenv()


class Config:
    """
    Base configuration class
    """

    # =========================
    # FLASK CORE SECURITY
    # =========================
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    # =========================
    # DATABASE
    # =========================
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # =========================
    # JWT CONFIGURATION
    # =========================
    JWT_ACCESS_TOKEN_EXPIRES = int(
        os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600)
    )  # 1 hour

    JWT_REFRESH_TOKEN_EXPIRES = int(
        os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 2592000)
    )  # 30 days

    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"

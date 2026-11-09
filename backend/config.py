import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()


class Config:
    """Central configuration loader for backend environment variables."""

    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    PORT = int(os.getenv("FLASK_PORT", 5000))
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # SQL Database URI (defaults to local SQLite so app runs out-of-the-box)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///cd_store.db")

    # MongoDB configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "cd_store_nosql")

    # External AI / Chat service credentials
    AI_API_KEY = os.getenv("AI_API_KEY", "")
    AI_API_URL = os.getenv("AI_API_URL", "")


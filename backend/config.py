import os
from pathlib import Path
from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent

# Load environment variables strictly from backend/.env
load_dotenv(dotenv_path=BACKEND_DIR / ".env")


class Config:
    """Central configuration loader for backend environment variables."""

    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    PORT = int(os.getenv("FLASK_PORT", 5000))
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    JWT_SECRET = os.getenv("JWT_SECRET", SECRET_KEY)

    # SQL Database URI (Neon Postgres DATABASE_URL from backend/.env, with SQLite fallback)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///cd_store.db")
    DATABASE_URL_UNPOOLED = os.getenv("DATABASE_URL_UNPOOLED", DATABASE_URL)

    # MongoDB configuration linked to backend/.env variables
    MONGODB_USERNAME = os.getenv("MONGODB_USERNAME", "")
    MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "")
    MONGODB_URI = os.getenv(
        "MONGODB_ATLAS_URI",
        os.getenv("MONGODB_URI", os.getenv("MONGO_URI", "mongodb://localhost:27017/")),
    )
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "cd_store_nosql")

    # Keep MONGO_URI alias for backwards compatibility
    MONGO_URI = MONGODB_URI

    # External AI / Chat service credentials
    AI_API_KEY = os.getenv("AI_API_KEY", "")
    AI_API_URL = os.getenv("AI_API_URL", "")

from datetime import datetime, timezone
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from config import Config

# Initialize MongoClient (lazy connection)
mongo_client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=2000)
mongo_db = mongo_client[Config.MONGO_DB_NAME]
chat_logs_collection = mongo_db["chat_logs"]


def log_chat_interaction(user_message: str, bot_reply: str, session_id: str = "anonymous") -> dict:
    """
    Helper stub to log AI chat interactions into MongoDB.
    Gracefully handles connection failures when MongoDB is not running locally.
    """
    document = {
        "session_id": session_id,
        "user_message": user_message,
        "bot_reply": bot_reply,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    try:
        result = chat_logs_collection.insert_one(document)
        document["_id"] = str(result.inserted_id)
        document["persisted"] = True
    except PyMongoError:
        # Fallback stub behavior if MongoDB server isn't reachable
        document["persisted"] = False

    return document


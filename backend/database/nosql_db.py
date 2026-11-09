import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from dotenv import load_dotenv
from pymongo import DESCENDING, MongoClient
from pymongo.errors import PyMongoError

# Ensure backend directory is on sys.path when running this file directly
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# Load connection string from backend/.env
load_dotenv(dotenv_path=BACKEND_DIR / ".env")


def get_mongo_client() -> MongoClient:
    """
    Create and return a MongoClient using MONGODB_ATLAS_URI or MONGODB_URI from backend/.env.
    """
    mongo_uri = os.getenv("MONGODB_ATLAS_URI") or os.getenv("MONGODB_URI")
    if not mongo_uri:
        raise ValueError("MONGODB_ATLAS_URI / MONGODB_URI is missing from backend/.env")
    return MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)


def ping_nosql() -> tuple[bool, str]:
    """
    Pings the MongoDB Atlas cluster to verify connection status.
    Returns (True, message) if successful, or (False, error) on failure.
    """
    try:
        client = get_mongo_client()
        client.admin.command("ping")
        return True, "MongoDB Atlas is reachable and connected!"
    except Exception as e:
        return False, str(e)


def get_nosql_db():
    """Return the MongoDB database instance containing chat_sessions and system_logs."""
    db_name = os.getenv("MONGO_DB_NAME", "cd_store_nosql")
    return get_mongo_client()[db_name]


# =====================================================================
# 1. CHAT SESSIONS HANDLERS (chat_sessions collection)
# =====================================================================

def log_chat_session(
    session_id: str,
    user_message: str,
    bot_reply: str,
    metadata: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """
    Create or append to a conversation in the `chat_sessions` collection.
    """
    now = datetime.now(timezone.utc).isoformat()
    message_entry = {
        "user_message": user_message,
        "bot_reply": bot_reply,
        "timestamp": now,
    }

    update_doc: dict[str, Any] = {
        "$setOnInsert": {
            "session_id": session_id,
            "created_at": now,
        },
        "$set": {
            "updated_at": now,
            "metadata": metadata or {},
        },
        "$push": {
            "messages": message_entry,
        },
    }

    result_payload: dict[str, Any] = {
        "session_id": session_id,
        "latest_exchange": message_entry,
        "persisted": False,
    }

    try:
        db = get_nosql_db()
        db["chat_sessions"].update_one(
            {"session_id": session_id},
            update_doc,
            upsert=True,
        )
        result_payload["persisted"] = True
    except (PyMongoError, ValueError) as exc:
        result_payload["error"] = str(exc)

    return result_payload


def get_chat_session(session_id: str) -> Optional[dict[str, Any]]:
    """Retrieve a chat session document by `session_id` from `chat_sessions`."""
    try:
        db = get_nosql_db()
        doc = db["chat_sessions"].find_one({"session_id": session_id})
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc
    except (PyMongoError, ValueError):
        return None


def log_chat_interaction(
    user_message: str, bot_reply: str, session_id: str = "anonymous"
) -> dict[str, Any]:
    """Convenience wrapper that logs a chat interaction to `chat_sessions`."""
    return log_chat_session(
        session_id=session_id,
        user_message=user_message,
        bot_reply=bot_reply,
    )


# =====================================================================
# 2. SYSTEM LOGS HANDLERS (system_logs collection)
# =====================================================================

def log_system_event(
    event_type: str,
    message: str,
    level: str = "INFO",
    details: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """
    Insert a system event/diagnostic log into the `system_logs` collection.
    """
    log_entry: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": level.upper(),
        "event_type": event_type,
        "message": message,
        "details": details or {},
    }

    try:
        db = get_nosql_db()
        result = db["system_logs"].insert_one(log_entry)
        log_entry["_id"] = str(result.inserted_id)
        log_entry["persisted"] = True
    except (PyMongoError, ValueError) as exc:
        log_entry["persisted"] = False
        log_entry["error"] = str(exc)

    return log_entry


def get_system_logs(
    limit: int = 50, level: Optional[str] = None
) -> list[dict[str, Any]]:
    """Retrieve the most recent system logs from the `system_logs` collection."""
    query: dict[str, Any] = {}
    if level:
        query["level"] = level.upper()

    try:
        db = get_nosql_db()
        cursor = (
            db["system_logs"]
            .find(query)
            .sort("timestamp", DESCENDING)
            .limit(limit)
        )
        logs = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            logs.append(doc)
        return logs
    except (PyMongoError, ValueError):
        return []


if __name__ == "__main__":
    ok, msg = ping_nosql()
    print(f"Ping status: {ok} - {msg}")

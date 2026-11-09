from datetime import datetime, timezone
import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient

BACKEND_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BACKEND_DIR / ".env")


def get_mongo_client():
  mongo_uri = os.getenv("MONGODB_ATLAS_URI") or os.getenv("MONGODB_URI")
  if not mongo_uri:
    raise ValueError("MONGODB_ATLAS_URI is missing from backend/.env")
  return MongoClient(mongo_uri)


def get_nosql_db():
  client = get_mongo_client()
  return client["cd_store"]


def ping_nosql():
  """Verifies connection to MongoDB Atlas."""
  try:
    client = get_mongo_client()
    client.admin.command("ping")
    return True, "MongoDB Atlas connected successfully!"
  except Exception as e:
    return False, str(e)


def save_chat_message(session_id, user_message, bot_reply):
  """Saves user/bot chat thread into the 'chat_sessions' collection."""
  db = get_nosql_db()
  chats = db["chat_sessions"]
  timestamp = datetime.now(timezone.utc).isoformat()
  chats.update_one(
      {"session_id": session_id},
      {
          "$push": {
              "messages": {
                  "user": user_message,
                  "bot": bot_reply,
                  "timestamp": timestamp,
              }
          },
          "$setOnInsert": {"created_at": timestamp, "session_id": session_id},
      },
      upsert=True,
  )


def get_chat_history(session_id):
  """Fetches chat history for prompt context injection."""
  db = get_nosql_db()
  session_doc = db["chat_sessions"].find_one({"session_id": session_id})
  if session_doc and "messages" in session_doc:
    return session_doc["messages"]
  return []


def get_album_extra_details(cd_id):
  """Fetches tracklist and extra metadata for a given cd_id from NoSQL."""
  db = get_nosql_db()
  details = db["cd_extra_details"].find_one({"cd_id": int(cd_id)}, {"_id": 0})
  return details or {}


def log_system_event(event_type, details):
  """Logs background system and LLM performance metrics."""
  db = get_nosql_db()
  db["system_logs"].insert_one({
      "event_type": event_type,
      "details": details,
      "timestamp": datetime.now(timezone.utc).isoformat(),
  })
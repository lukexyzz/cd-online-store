from database.nosql_db import log_system_event, save_chat_message
from flask import Blueprint, jsonify, request

chat_bp = Blueprint("chat_routes", __name__)


@chat_bp.route("/chat", methods=["POST"])
def handle_chat():
  data = request.get_json() or {}
  user_message = data.get("message", "").strip()
  session_id = data.get("session_id", "default_session")

  if not user_message:
    return jsonify({"error": "Message body is required"}), 400

  # RAG Response Stub (Injecting Store Guidance)
  bot_reply = (
      f"AI Assistant: Thanks for asking! Our store carries heavy music CDs"
      f" like Contention, Cauldron, and Long Goodbye. Regarding your question"
      f" '{user_message}': You can add any album to your cart and proceed to"
      f" checkout!"
  )

  # Save user/bot interaction into MongoDB chat_sessions collection
  save_chat_message(session_id, user_message, bot_reply)

  # Log the interaction event in MongoDB system_logs collection
  log_system_event(
      "CHAT_INTERACTION",
      {"session_id": session_id, "prompt_length": len(user_message)},
  )

  return jsonify({"reply": bot_reply}), 200
from flask import Blueprint, jsonify, request
from database.nosql_db import log_chat_interaction

chat_bp = Blueprint("chat_routes", __name__)


@chat_bp.route("/api/chat", methods=["POST"])
def chat_assistant():
    """POST /api/chat route stub for AI store assistant queries."""
    payload = request.get_json(silent=True) or {}
    user_message = payload.get("message", "").strip()

    if not user_message:
        return jsonify({"status": "error", "message": "Message field is required."}), 400

    # Stub AI reply
    bot_reply = (
        f"Thanks for asking about '{user_message}'! "
        "I'm your CD Store AI assistant stub. Check out Pink Floyd or Daft Punk in our catalog!"
    )

    log_entry = log_chat_interaction(user_message=user_message, bot_reply=bot_reply)

    return (
        jsonify(
            {
                "status": "success",
                "reply": bot_reply,
                "logged": log_entry.get("persisted", False),
            }
        ),
        200,
    )


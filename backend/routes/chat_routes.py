from flask import Blueprint, jsonify, request
from database.nosql_db import log_chat_session, log_system_event

chat_bp = Blueprint("chat_routes", __name__)


@chat_bp.route("/api/chat", methods=["POST"])
def chat_assistant():
    """POST /api/chat route stub for AI store assistant queries."""
    payload = request.get_json(silent=True) or {}
    user_message = payload.get("message", "").strip()
    session_id = payload.get("session_id", "default-session")

    if not user_message:
        log_system_event(
            event_type="CHAT_VALIDATION_ERROR",
            message="Empty chat message submitted",
            level="WARNING",
        )
        return jsonify({"status": "error", "message": "Message field is required."}), 400

    # Stub AI reply
    bot_reply = (
        f"Thanks for asking about '{user_message}'! "
        "I'm your CD Store AI assistant stub. Check out Pink Floyd or Daft Punk in our catalog!"
    )

    session_entry = log_chat_session(
        session_id=session_id,
        user_message=user_message,
        bot_reply=bot_reply,
    )
    log_system_event(
        event_type="CHAT_MESSAGE_PROCESSED",
        message=f"Processed chat message for session '{session_id}'",
        level="INFO",
        details={"session_id": session_id},
    )

    return (
        jsonify(
            {
                "status": "success",
                "session_id": session_id,
                "reply": bot_reply,
                "logged": session_entry.get("persisted", False),
            }
        ),
        200,
    )

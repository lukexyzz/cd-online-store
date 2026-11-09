from flask import Blueprint, jsonify, request
from database.nosql_db import log_system_event

order_bp = Blueprint("order_routes", __name__)


@order_bp.route("/api/orders", methods=["POST"])
def create_order():
    """POST /api/orders route stub to process a customer order."""
    payload = request.get_json(silent=True) or {}
    items = payload.get("items", [])

    if not items:
        log_system_event(
            event_type="ORDER_VALIDATION_ERROR",
            message="Order attempted with empty items list",
            level="WARNING",
        )
        return jsonify({"status": "error", "message": "Order must contain at least one item."}), 400

    total = round(sum(item.get("price", 0) * item.get("quantity", 1) for item in items), 2)
    order_id = "ORD-1001"

    log_system_event(
        event_type="ORDER_CREATED",
        message=f"Order {order_id} created",
        level="INFO",
        details={"order_id": order_id, "item_count": len(items), "total": total},
    )

    return (
        jsonify(
            {
                "status": "success",
                "message": "Order placed successfully (stub).",
                "order": {
                    "order_id": order_id,
                    "items": items,
                    "total": total,
                },
            }
        ),
        201,
    )

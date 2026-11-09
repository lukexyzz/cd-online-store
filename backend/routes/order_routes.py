from flask import Blueprint, jsonify, request

order_bp = Blueprint("order_routes", __name__)


@order_bp.route("/api/orders", methods=["POST"])
def create_order():
    """POST /api/orders route stub to process a customer order."""
    payload = request.get_json(silent=True) or {}
    items = payload.get("items", [])

    if not items:
        return jsonify({"status": "error", "message": "Order must contain at least one item."}), 400

    total = sum(item.get("price", 0) * item.get("quantity", 1) for item in items)

    return (
        jsonify(
            {
                "status": "success",
                "message": "Order placed successfully (stub).",
                "order": {
                    "order_id": "ORD-1001",
                    "items": items,
                    "total": round(total, 2),
                },
            }
        ),
        201,
    )


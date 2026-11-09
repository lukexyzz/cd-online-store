from flask import Blueprint, jsonify

cd_bp = Blueprint("cd_routes", __name__)

# Starter sample catalog data for out-of-the-box functionality
SAMPLE_CDS = [
    {
        "id": 1,
        "title": "Dark Side of the Moon",
        "artist": "Pink Floyd",
        "genre": "Progressive Rock",
        "price": 14.99,
        "stock": 12,
    },
    {
        "id": 2,
        "title": "Discovery",
        "artist": "Daft Punk",
        "genre": "Electronic",
        "price": 12.99,
        "stock": 8,
    },
    {
        "id": 3,
        "title": "Kind of Blue",
        "artist": "Miles Davis",
        "genre": "Jazz",
        "price": 11.49,
        "stock": 5,
    },
    {
        "id": 4,
        "title": "Rumours",
        "artist": "Fleetwood Mac",
        "genre": "Rock",
        "price": 13.99,
        "stock": 15,
    },
]


@cd_bp.route("/api/cds", methods=["GET"])
def get_cds():
    """GET /api/cds route stub returning the CD catalog."""
    return jsonify({"status": "success", "data": SAMPLE_CDS}), 200


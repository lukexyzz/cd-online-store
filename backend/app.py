import os
import sys

# Ensure backend directory is on sys.path for consistent imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from database.nosql_db import ping_nosql
from routes.cd_routes import cd_bp
from routes.chat_routes import chat_bp
from routes.order_routes import order_bp


def create_app() -> Flask:
    """Application factory for the CD Online Store Flask REST API."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS so your React frontend (e.g. http://localhost:5173) can communicate with Flask
    CORS(app)

    # Register API blueprints
    app.register_blueprint(cd_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(chat_bp)

    @app.route("/api/ping-db", methods=["GET"])
    def ping_db():
        ok, message = ping_nosql()
        if ok:
            return jsonify({"ok": True, "message": message}), 200
        return jsonify({"ok": False, "error": message}), 500

    @app.route("/api/health", methods=["GET"])
    def health_check():
        """Health check endpoint."""
        return jsonify({"status": "healthy", "service": "cd-online-store-api"}), 200

    @app.route("/")
    def index():
        return "Flask REST API + MongoDB is running. Try GET /api/ping-db"

    return app


app = create_app()

if __name__ == "__main__":
    app.run(port=5000, debug=True)

import os
import sys

# Ensure backend directory is on sys.path for consistent imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from routes.cd_routes import cd_bp
from routes.chat_routes import chat_bp
from routes.order_routes import order_bp


def create_app() -> Flask:
    """Application factory for the CD Online Store Flask REST API."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for decoupled React frontend
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register API blueprints
    app.register_blueprint(cd_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(chat_bp)

    @app.route("/api/health", methods=["GET"])
    def health_check():
        """Health check endpoint."""
        return jsonify({"status": "healthy", "service": "cd-online-store-api"}), 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT, debug=(Config.FLASK_ENV == "development"))


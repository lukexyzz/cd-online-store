import os
import sys

# Ensure backend directory is on sys.path for consistent imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from database.nosql_db import ping_nosql
from database.sql_db import ping_sql
from flask import Flask, jsonify
from flask_cors import CORS

# Import Blueprints
from routes.auth_routes import auth_bp
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
  app.register_blueprint(auth_bp)
  app.register_blueprint(cd_bp)
  app.register_blueprint(order_bp)
  app.register_blueprint(chat_bp)

  @app.route("/api/ping-db", methods=["GET"])
  def ping_db():
    sql_ok, sql_message = ping_sql()
    nosql_ok, nosql_message = ping_nosql()
    both_ok = sql_ok and nosql_ok
    response_payload = {
        "ok": both_ok,
        "message": f"{sql_message} | {nosql_message}",
        "sql": {"ok": sql_ok, "message": sql_message},
        "nosql": {"ok": nosql_ok, "message": nosql_message},
    }
    return jsonify(response_payload), (200 if both_ok else 500)

  @app.route("/api/health", methods=["GET"])
  def health_check():
    """Health check endpoint."""
    return (
        jsonify({"status": "healthy", "service": "cd-online-store-api"}),
        200,
    )

  @app.route("/")
  def index():
    return "Flask REST API + Neon SQL + MongoDB is running. Try GET /api/ping-db"

  return app


app = create_app()

if __name__ == "__main__":
  app.run(port=5000, debug=True)
from datetime import datetime, timedelta, timezone
import os
from config import Config
from database.sql_db import User, get_sql_session
from flask import Blueprint, jsonify, request
import jwt
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint("auth_routes", __name__, url_prefix="/api")

JWT_SECRET = os.getenv("JWT_SECRET", Config.SECRET_KEY)


def generate_token(user: User) -> str:
  """Generates a signed JWT token valid for 24 hours."""
  now = datetime.now(timezone.utc)
  payload = {
      "user_id": user.user_id,
      "email": user.email,
      "role": user.role,
      "iat": now,
      "exp": now + timedelta(hours=24),
  }
  return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


@auth_bp.route("/auth/register", methods=["POST"])
def register():
  data = request.get_json() or {}
  email = data.get("email", "").strip()
  password = data.get("password", "")

  if not email or not password:
    return jsonify({"error": "Email and password are required."}), 400

  session = get_sql_session()
  existing_user = session.query(User).filter(User.email == email).first()
  if existing_user:
    session.close()
    return jsonify({"error": "User already exists."}), 400

  hashed_pw = generate_password_hash(password)
  new_user = User(email=email, password_hash=hashed_pw, role="customer")
  session.add(new_user)
  session.commit()

  user_dict = new_user.to_dict()
  session.close()

  return jsonify({"message": "Registered successfully!", "user": user_dict}), 201


@auth_bp.route("/auth/login", methods=["POST"])
def login():
  data = request.get_json() or {}
  email = data.get("email", "").strip()
  password = data.get("password", "")

  if not email or not password:
    return jsonify({"error": "Email and password are required."}), 400

  session = get_sql_session()
  user = session.query(User).filter(User.email == email).first()

  if not user or not check_password_hash(str(user.password_hash), password):
    session.close()
    return jsonify({"error": "Invalid email or password."}), 401

  # Issue JWT token on successful login
  token = generate_token(user)

  user_dict = user.to_dict()
  session.close()

  return (
      jsonify({
          "message": "Login successful!",
          "token": token,
          "user": user_dict,
      }),
      200,
  )

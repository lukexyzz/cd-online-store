from database.nosql_db import get_album_extra_details
from database.sql_db import CD, get_sql_session
from flask import Blueprint, jsonify

cd_bp = Blueprint("cd_routes", __name__)


# GET /api/cds -> Returns basic catalog from SQL
@cd_bp.route("/cds", methods=["GET"])
def get_all_cds():
  session = get_sql_session()
  cds = session.query(CD).all()
  result = [cd.to_dict() for cd in cds]
  session.close()
  return jsonify(result), 200


# GET /api/cds/<int:cd_id> -> Returns combined SQL catalog data & NoSQL extra details
@cd_bp.route("/cds/<int:cd_id>", methods=["GET"])
def get_cd_by_id(cd_id):
  session = get_sql_session()
  cd = session.query(CD).filter(CD.cd_id == cd_id).first()

  if not cd:
    session.close()
    return jsonify({"error": "CD not found"}), 404

  cd_data = cd.to_dict()
  session.close()

  # Fetch extra details (tracklist, label, tags) from NoSQL
  extra_details = get_album_extra_details(cd_id)

  # Merge both dictionaries into a single comprehensive response
  combined_data = {**cd_data, **extra_details}

  return jsonify(combined_data), 200
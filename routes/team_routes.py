from flask import Blueprint, jsonify
from services.fetch_team import fetch_team_members

team_bp = Blueprint('team', __name__)

@team_bp.route('/api/team', methods=['GET'])
def get_team():
    try:
        members = fetch_team_members()
        return jsonify(members)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
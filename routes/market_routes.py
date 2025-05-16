from flask import Blueprint, jsonify
from services.market_dao import fetch_market_data

market_bp = Blueprint('market', __name__)

@market_bp.route('/api/market', methods=['GET'])
def get_market_data():
    try:
        result = fetch_market_data()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

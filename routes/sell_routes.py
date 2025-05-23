from flask import Blueprint, request, jsonify
from schemas.sell import SellRequest
from services.transaction_dao import add_transaction

sell_bp = Blueprint('sell', __name__)

@sell_bp.route('/sell', methods=['POST'])
def sell_stock():
    try:
        data = request.get_json()
        sell_request = SellRequest(**data)

        transaction_id = add_transaction(
            portfolio_id=sell_request.portfolio_id,
            ticker=sell_request.ticker,
            quantity=-abs(sell_request.quantity),  # negative for sell
            price=sell_request.price,
            transaction_type="SELL"
        )
        return jsonify({
            "message": "Stock sold successfully",
            "transaction_id": transaction_id
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


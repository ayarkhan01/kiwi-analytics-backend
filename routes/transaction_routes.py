from flask import Blueprint, jsonify

transactions_bp = Blueprint('transactions', __name__, url_prefix='/api')

@transactions_bp.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = [
        {
            "id": 201,
            "portfolio": "Retirement",
            "ticker": "MSFT",
            "type": "Buy",
            "quantity": 8,
            "price": 330.12,
            "dateTime": "2024-11-01T09:30:00"
        },
        {
            "id": 202,
            "portfolio": "Growth",
            "ticker": "AAPL",
            "type": "Sell",
            "quantity": 4,
            "price": 198.76,
            "dateTime": "2024-11-02T14:45:00"
        }
    ]
    return jsonify(transactions)

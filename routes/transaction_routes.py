from flask import Blueprint, jsonify, request

transactions_bp = Blueprint('transactions', __name__, url_prefix='/api')

# Simulated in-memory transactions list
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

@transactions_bp.route('/transactions', methods=['GET'])
def get_transactions():
    return jsonify(transactions)

@transactions_bp.route('/transactions', methods=['POST'])
def add_transaction():
    new_txn = request.get_json()

    # Basic validation 
    required_fields = {"portfolio", "ticker", "type", "quantity", "price", "dateTime"}
    if not new_txn or not required_fields.issubset(new_txn.keys()):
        return jsonify({"error": "Missing required fields"}), 400

    # Optional: Validate type is 'Buy' or 'Sell'
    if new_txn['type'] not in ['Buy', 'Sell']:
        return jsonify({"error": "Transaction type must be 'Buy' or 'Sell'"}), 400

    # Assign a new ID - just increment max id for demo
    max_id = max(t['id'] for t in transactions) if transactions else 200
    new_txn['id'] = max_id + 1

    transactions.append(new_txn)
    return jsonify(new_txn), 201

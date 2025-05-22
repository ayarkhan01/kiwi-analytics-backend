from flask import Blueprint, jsonify, request
from services.portfolio_dao import get_portfolios_by_user
from services.transaction_dao import get_transactions_for_portfolio

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/api/transactions', methods=['POST'])
def get_user_transactions():
    try:
        data = request.get_json()
        user_id = data.get('user_id')

        if not user_id:
            return jsonify({"error": "user_id is required"}), 400

        # Get all portfolios for the user
        portfolios = get_portfolios_by_user(user_id)
        
        # Get transactions for each portfolio
        all_transactions = []
        for portfolio in portfolios:
            portfolio_transactions = get_transactions_for_portfolio(portfolio.id)
            # Add portfolio info to each transaction
            for transaction in portfolio_transactions:
                transaction['portfolio_id'] = portfolio.id
                transaction['portfolio_name'] = portfolio.name
            all_transactions.extend(portfolio_transactions)

        # Sort transactions by executed_at in descending order (most recent first)
        all_transactions.sort(key=lambda x: x['executed_at'], reverse=True)

        return jsonify(all_transactions), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

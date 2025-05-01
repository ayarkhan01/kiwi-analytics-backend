from flask import Blueprint, request, jsonify, g
from services.portfolio_dao import (
    get_portfolios_by_user, 
    get_portfolio_by_id,
    create_portfolio, 
    update_portfolio_name,
    delete_portfolio
)
from services.position_dao import (
    buy_stock,
    sell_stock
)
from services.transaction_dao import get_transactions_for_portfolio
from models.portfolio import StrategyEnum
from middleware import auth_required  # Import the middleware

portfolio_bp = Blueprint('portfolio', __name__)

# Add a new route for getting the current user's portfolios
@portfolio_bp.route('/api/portfolios/user', methods=['GET'])
@auth_required  # Apply the decorator here
def get_current_user_portfolios():
    user_id = g.user_id  # Get the authenticated user ID from the middleware
    try:
        portfolios = get_portfolios_by_user(user_id)
        return jsonify([{
            'id': p.id,
            'name': p.name,
            'strategy': p.strategy.value,
            'created_at': p.created_at.isoformat() if p.created_at else None
        } for p in portfolios])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# You can also protect your existing routes
@portfolio_bp.route('/api/portfolios/add', methods=['POST'])
@auth_required  # Apply here too if you want
def add_portfolio():
    data = request.json
    try:
        # You could use g.user_id instead of getting it from the request
        # user_id = g.user_id
        strategy = StrategyEnum[data.get('strategy')]
        portfolio = create_portfolio(
            user_id=data.get('user_id'),
            name=data.get('name'),
            strategy=strategy
        )
        return jsonify({
            'id': portfolio.id,
            'name': portfolio.name,
            'strategy': portfolio.strategy.value,
            'created_at': portfolio.created_at.isoformat() if portfolio.created_at else None
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Keep your other routes...
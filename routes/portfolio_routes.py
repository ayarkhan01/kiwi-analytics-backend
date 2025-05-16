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
from models.portfolio import Portfolio, StrategyEnum
from services.market_dao import fetch_market_data
from services.position_dao import get_positions_by_portfolio

portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/api/portfolios/user', methods=['POST'])
def get_current_user_portfolios():
    try:
        data = request.get_json()
        user_id = data.get('user_id')

        if not user_id:
            return jsonify({"error": "user_id is required"}), 400
            
        # Get user's portfolios - FIXED: use get_portfolios_by_user instead of get_portfolio_by_id
        portfolios = get_portfolios_by_user(user_id)
        
        # We don't need this check anymore since get_portfolios_by_user always returns a list
        # but keeping it for extra safety
        if not isinstance(portfolios, list):
            portfolios = [portfolios]
        
        market_data = fetch_market_data()
        stock_lookup = {s["ticker"]: s for s in market_data}

        def calculate_position_metrics(quantity, avg_price, current_price):
            market_value = quantity * current_price
            cost_basis = quantity * avg_price
            profit_loss = market_value - cost_basis
            profit_loss_percent = ((current_price - avg_price) / avg_price) * 100 if avg_price != 0 else 0
            return market_value, cost_basis, profit_loss, profit_loss_percent

        portfolio_summary = []

        for portfolio in portfolios:
            positions = get_positions_by_portfolio(portfolio.id)
            positions_list = []
            
            for p in positions:
                # Convert SQLAlchemy model to dictionary to avoid session issues
                ticker = p.ticker
                position_id = p.id
                quantity = p.quantity
                average_price = float(p.average_price)
                created_at = p.created_at.isoformat() if hasattr(p, 'created_at') and p.created_at else None
                updated_at = p.updated_at.isoformat() if hasattr(p, 'updated_at') and p.updated_at else None
                
                stock_info = stock_lookup.get(ticker, {})
                current_price = stock_info.get("price", 0)
                mv, cb, pnl, pnl_pct = calculate_position_metrics(quantity, average_price, current_price)

                positions_list.append({
                    "id": position_id,
                    "ticker": ticker,
                    "name": stock_info.get("name", ticker),
                    "sector": stock_info.get("sector", "Unknown"),
                    "quantity": quantity,
                    "average_price": average_price,
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "current_price": current_price,
                    "market_value": round(mv, 2),
                    "cost_basis": round(cb, 2),
                    "profit_loss": round(pnl, 2),
                    "profit_loss_percent": round(pnl_pct, 2),
                    "percent_change": stock_info.get("change", 0),
                    "market_cap": stock_info.get("marketCap", "N/A")
                })

            portfolio_summary.append({
                "portfolio_id": portfolio.id,
                "portfolio_name": portfolio.name,
                "strategy": portfolio.strategy.value if hasattr(portfolio.strategy, 'value') else portfolio.strategy,
                "positions": positions_list
            })

        return jsonify(portfolio_summary), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@portfolio_bp.route('/api/portfolios/add', methods=['POST'])
def add_portfolio():
    data = request.json
    try:
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
    
@portfolio_bp.route('/api/portfolios/buy', methods=['POST'])
def buy_stock_route():
    try:
        data = request.json
        result = buy_stock(
            portfolio_id=data['portfolio_id'],
            ticker=data['ticker'],
            quantity=data['quantity'],
            price=data['price']
        )
        return jsonify({"message": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
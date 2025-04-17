from db import get_session
from models.portfolio import Portfolio, StrategyEnum

def create_portfolio(user_id, name, strategy: StrategyEnum):
    portfolio = Portfolio(user_id=user_id, name=name, strategy=strategy)
    with get_session() as session:
        session.add(portfolio)
        session.flush()  # returns portfolio.id if needed
        return portfolio

def delete_portfolio(portfolio_id):
    with get_session() as session:
        portfolio = session.query(Portfolio).get(portfolio_id)
        if portfolio:
            session.delete(portfolio)

def get_portfolios_by_user(user_id):
    with get_session() as session:
        return session.query(Portfolio).filter_by(user_id=user_id).all()
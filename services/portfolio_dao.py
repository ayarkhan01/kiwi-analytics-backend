from db import get_session
from models.portfolio import Portfolio, StrategyEnum

def get_portfolio_by_id(portfolio_id):
    with get_session() as session:
        portfolio = session.get(Portfolio, portfolio_id)  # preferred over .query(...).get()
        if portfolio:
            # Access all relevant attributes to load them
            _ = portfolio.id, portfolio.user_id, portfolio.name, portfolio.strategy, portfolio.created_at, portfolio.updated_at
            session.expunge(portfolio)  # Detach from session
        return portfolio
    
def get_portfolios_by_user(user_id):
    with get_session() as session:
        portfolios = session.query(Portfolio).filter_by(user_id=user_id).all()
        
        # Ensure all attributes are loaded while the session is active
        for p in portfolios:
            # Access attributes you plan to use
            _ = p.id, p.user_id, p.name, p.strategy, p.created_at, p.updated_at
            session.expunge(p)  # Detach the object cleanly from session

        return portfolios

def create_portfolio(user_id, name, strategy: StrategyEnum):
    portfolio = Portfolio(user_id=user_id, name=name, strategy=strategy)
    with get_session() as session:
        session.add(portfolio)
        session.flush()       # Sends INSERT to DB so the ID is generated
        session.refresh(portfolio)  # Loads DB-generated fields like created_at, updated_at
        session.expunge(portfolio)  # Detach from session to avoid DetachedInstanceError later
        return portfolio

def delete_portfolio(portfolio_id):
    with get_session() as session:
        portfolio = get_portfolio_by_id(portfolio_id)
        if portfolio:
            session.delete(portfolio)

def update_portfolio_name(portfolio_id, new_name):
    with get_session() as session:
        portfolio = session.get(Portfolio, portfolio_id)
        if portfolio:
            portfolio.name = new_name
            session.flush()
            session.refresh(portfolio)
            session.expunge(portfolio)
            return portfolio

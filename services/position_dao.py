from db import get_session
from models.positions import Position

def add_or_update_position(portfolio_id, ticker, quantity, price):
    with get_session() as session:
        position = session.query(Position).filter_by(portfolio_id=portfolio_id, ticker=ticker).first()
        if position:
            total_quantity = position.quantity + quantity
            if total_quantity == 0:
                position.average_price = 0
            else:
                position.average_price = ((position.average_price * position.quantity) + (price * quantity)) / total_quantity
            position.quantity = total_quantity
        else:
            position = Position(
                portfolio_id=portfolio_id,
                ticker=ticker,
                quantity=quantity,
                average_price=price
            )
            session.add(position)
        return position

def get_positions_by_portfolio(portfolio_id):
    """
    Fetch all positions (holdings) for a specific portfolio.
    """
    with get_session() as session:
        return session.query(Position).filter_by(portfolio_id=portfolio_id).all()

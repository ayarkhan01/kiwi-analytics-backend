from decimal import Decimal
from db import get_session
from models.positions import Position
from services.transaction_dao import add_transaction
from models.transactions import TransactionType

def get_positions_by_portfolio(portfolio_id):
    with get_session() as session:
        positions = session.query(Position).filter_by(portfolio_id=portfolio_id).all()
        
        # Force-load the attributes before the session closes
        for p in positions:
            _ = p.id, p.ticker, p.quantity, p.average_price, p.created_at, p.updated_at

        return positions



def buy_stock(portfolio_id, ticker, quantity, price):
    price = Decimal(str(price))

    with get_session() as session:
        position = session.query(Position).filter_by(
            portfolio_id=portfolio_id,
            ticker=ticker
        ).first()

        if position:
            total_quantity = position.quantity + quantity
            position.average_price = (
                (position.average_price * position.quantity) + (price * quantity)
            ) / total_quantity
            position.quantity = total_quantity
        else:
            position = Position(
                portfolio_id=portfolio_id,
                ticker=ticker,
                quantity=quantity,
                average_price=price
            )
            session.add(position)

        session.commit()

        # Log the transaction
        add_transaction(
            portfolio_id=portfolio_id,
            ticker=ticker,
            quantity=quantity,
            price=price,
            transaction_type=TransactionType.buy
        )

        return f"Successfully bought {quantity} shares of {ticker} at ${float(price):.2f}"


def sell_stock(portfolio_id, ticker, quantity, price):
    price = Decimal(str(price))

    with get_session() as session:
        position = session.query(Position).filter_by(
            portfolio_id=portfolio_id,
            ticker=ticker
        ).first()

        if not position or position.quantity < quantity:
            raise ValueError("Not enough shares to sell.")

        position.quantity -= quantity

        if position.quantity == 0:
            position.average_price = 0

        session.commit()

        # Log the transaction
        add_transaction(
            portfolio_id=portfolio_id,
            ticker=ticker,
            quantity=quantity,
            price=price,
            transaction_type=TransactionType.sell
        )

        return f"Successfully sold {quantity} shares of {ticker} at ${float(price):.2f}"

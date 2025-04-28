from models.positions import Position
from models.transactions import Transaction, TransactionType
from services.transaction_dao import add_transaction
from db import get_session
from decimal import Decimal

def buy_stock(portfolio_id, ticker, quantity, price):
    price = Decimal(str(price))  # ✅ ensures safe Decimal conversion

    with get_session() as session:
        position = session.query(Position).filter_by(portfolio_id=portfolio_id, ticker=ticker).first()
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

        # Record transaction
        add_transaction(session, portfolio_id, ticker, quantity, price, TransactionType.buy)
        session.commit()
        return position

def sell_stock(portfolio_id, ticker, quantity, price):
    with get_session() as session:
        position = session.query(Position).filter_by(portfolio_id=portfolio_id, ticker=ticker).first()

        if not position or position.quantity < quantity:
            raise ValueError("Not enough shares to sell.")

        # Update position
        position.quantity -= quantity

        if position.quantity == 0:
            position.average_price = 0

        # Add transaction
        add_transaction(session, portfolio_id, ticker, quantity, price, TransactionType.sell)

        session.commit()
        return position
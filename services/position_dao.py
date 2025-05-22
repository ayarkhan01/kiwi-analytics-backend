from decimal import Decimal
from db import get_session
from models.positions import Position
from services.transaction_dao import add_transaction
from models.transactions import TransactionType
from services.user_dao import get_user_balance, update_user_balance
from models.portfolio import Portfolio

def get_positions_by_portfolio(portfolio_id):
    with get_session() as session:
        positions = session.query(Position).filter_by(portfolio_id=portfolio_id).all()
        
        for p in positions:
            _ = p.id, p.ticker, p.quantity, p.average_price, p.created_at, p.updated_at
            session.expunge(p)
            
        return positions

def buy_stock(portfolio_id, ticker, quantity, price):
    price = Decimal(str(price))
    quantity = Decimal(str(quantity))
    total_cost = quantity * price

    with get_session() as session:
        # Get the user_id from the portfolio
        portfolio = session.query(Portfolio).filter_by(id=portfolio_id).first()
        if not portfolio:
            raise ValueError("Portfolio not found")

        user_id = portfolio.user_id
        current_balance = Decimal(str(get_user_balance(user_id)))

        if current_balance < total_cost:
            raise ValueError("Insufficient balance to complete purchase")

        # Deduct from balance
        update_user_balance(user_id, current_balance - total_cost)

        # Proceed with stock purchase logic
        position = session.query(Position).filter_by(
            portfolio_id=portfolio_id,
            ticker=ticker
        ).first()

        if position:
            total_quantity = position.quantity + int(quantity)
            position.average_price = (
                (position.average_price * position.quantity) + (price * int(quantity))
            ) / total_quantity
            position.quantity = total_quantity
        else:
            position = Position(
                portfolio_id=portfolio_id,
                ticker=ticker,
                quantity=int(quantity),
                average_price=price
            )
            session.add(position)

    # Record transaction
    transaction_id = add_transaction(
        portfolio_id=portfolio_id,
        ticker=ticker,
        quantity=int(quantity),
        price=price,
        transaction_type=TransactionType.buy
    )

    return f"Successfully bought {int(quantity)} shares of {ticker} at ${float(price):.2f}"

def sell_stock(portfolio_id, ticker, quantity, price):
    price = Decimal(str(price))
    quantity = Decimal(str(quantity))
    total_proceeds = quantity * price

    with get_session() as session:
        position = session.query(Position).filter_by(
            portfolio_id=portfolio_id,
            ticker=ticker
        ).first()

        if not position or position.quantity < int(quantity):
            raise ValueError("Not enough shares to sell.")

        position.quantity -= int(quantity)

        if position.quantity == 0:
            position.average_price = 0

        # Add proceeds to balance
        portfolio = session.query(Portfolio).filter_by(id=portfolio_id).first()
        if not portfolio:
            raise ValueError("Portfolio not found")

        user_id = portfolio.user_id
        current_balance = Decimal(str(get_user_balance(user_id)))
        update_user_balance(user_id, current_balance + total_proceeds)

    # Record transaction
    transaction_id = add_transaction(
        portfolio_id=portfolio_id,
        ticker=ticker,
        quantity=int(quantity),
        price=price,
        transaction_type=TransactionType.sell
    )

    return f"Successfully sold {int(quantity)} shares of {ticker} at ${float(price):.2f}"

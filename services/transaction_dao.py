from db import get_session
from models.transactions import Transaction

def add_transaction(portfolio_id, ticker, quantity, price, transaction_type):
    with get_session() as session:    
        transaction = Transaction(
            portfolio_id=portfolio_id,
            ticker=ticker,
            transaction_type=transaction_type,
            quantity=quantity,
            price=price
        )
        session.add(transaction)
        # The session will be committed automatically when exiting the 'with' block
        # thanks to the context manager in db.py
        
        # Return the created transaction ID
        session.flush()  # This writes to DB and generates the ID
        transaction_id = transaction.id
        return transaction_id

def get_transactions_for_portfolio(portfolio_id):
    with get_session() as session:
        transactions = session.query(Transaction).filter_by(portfolio_id=portfolio_id).all()
        return [
            {
                "id": t.id,
                "ticker": t.ticker,
                "type": t.transaction_type.value,
                "quantity": t.quantity,
                "price": float(t.price),
                "executed_at": t.executed_at
            }
            for t in transactions
        ]
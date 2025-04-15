from db import get_session
from models.transactions import Transaction, TransactionType

def add_transaction(portfolio_id, ticker, quantity, price, transaction_type: TransactionType):
    transaction = Transaction(
        portfolio_id=portfolio_id,
        ticker=ticker,
        quantity=quantity,
        price=price,
        transaction_type=transaction_type
    )
    with get_session() as session:
        session.add(transaction)
        return transaction

def get_transactions_for_portfolio(portfolio_id):
    with get_session() as session:
        return session.query(Transaction).filter_by(portfolio_id=portfolio_id).all()

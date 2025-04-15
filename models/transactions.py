from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Enum, DateTime, func
from sqlalchemy.orm import relationship
from db import Base
import enum

class TransactionType(enum.Enum):
    buy = "buy"
    sell = "sell"

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'), nullable=False)
    ticker = Column(String(100), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(12, 2), nullable=False)
    executed_at = Column(DateTime, server_default=func.now())

    portfolio = relationship("Portfolio", backref="transactions")

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DECIMAL,
    DateTime,
    func,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from db import Base
from models.portfolio import Portfolio


class Position(Base):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'), nullable=False)
    ticker = Column(String(100), nullable=False)
    quantity = Column(Integer, default=0)
    average_price = Column(DECIMAL(12, 2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    portfolio = relationship(Portfolio, backref="positions")

    __table_args__ = (
        UniqueConstraint('portfolio_id', 'ticker', name='uq_portfolio_ticker'),
    )
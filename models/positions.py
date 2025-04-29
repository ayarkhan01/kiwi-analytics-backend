from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship
from db import Base
from models.portfolio import Portfolio
portfolio = relationship(Portfolio, backref="positions")


class Position(Base):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'), nullable=False)
    ticker = Column(String(100), nullable=False)
    quantity = Column(Integer, default=0)
    average_price = Column(DECIMAL(12, 2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (UniqueConstraint('portfolio_id', 'ticker', name='uq_portfolio_ticker'),)

    def __repr__(self):
        return (f"<Position(id={self.id}, portfolio_id={self.portfolio_id}, "
                f"ticker='{self.ticker}', quantity={self.quantity}, "
                f"average_price={self.average_price}, "
                f"created_at={self.created_at}, updated_at={self.updated_at})>")

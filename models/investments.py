from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from sqlalchemy.ext.declarative import declarative_base


class Investment(Base):
    __tablename__ = 'investments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    portfolio_id = Column(Integer, ForeignKey('portfolio.id'), nullable=False)
    ticker = Column(String(100), nullable=False)
    quantity = Column(Integer, default=0)
    price = Column(DECIMAL(10, 0), nullable=False)
    date = Column(DateTime, nullable=False)
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from db import Base
import enum

class StrategyEnum(enum.Enum):
    short_term = "short_term"
    long_term = "long_term"

class Portfolio(Base):
    __tablename__ = 'portfolios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(255), nullable=False)
    strategy = Column(Enum(StrategyEnum), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", backref="portfolios")

    def __repr__(self):
        return (f"<Portfolio(id={self.id}, user_id={self.user_id}, "
                f"name='{self.name}', strategy='{self.strategy.name}', "
                f"created_at={self.created_at}, updated_at={self.updated_at})>")

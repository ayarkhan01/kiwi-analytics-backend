from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Portfolio(Base):
    __tablename__ = 'portfolio'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(500), nullable=False)
    strategy = Column(String(100), nullable=False)

    def __str__(self):
        return f"Portfolio(id={self.id}, name='{self.name}', strategy='{self.strategy}')"
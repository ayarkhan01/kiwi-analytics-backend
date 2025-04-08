from sqlalchemy import Column, Integer, String, Boolean, DECIMAL
from db import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(200), unique=True, nullable=True)
    password = Column(String(200), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    balance = Column(DECIMAL(10, 0), nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', is_active={self.is_active}, balance={self.balance})>"
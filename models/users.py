from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, DateTime, func
from db import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(200), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    balance = Column(DECIMAL(12, 2), default=0.00)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

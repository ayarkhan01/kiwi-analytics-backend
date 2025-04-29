from sqlalchemy import Column, Integer, String, Text, DateTime, func
from db import Base 

class TeamMember(Base):
    __tablename__ = 'team_members'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    bio = Column(Text)
    photo_url = Column(String(255))

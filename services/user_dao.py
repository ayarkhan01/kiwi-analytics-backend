from db import get_session
from models.users import User

def create_user(username, password, balance=0.0):
    user = User(username=username, password=password, balance=balance)
    with get_session() as session:
        session.add(user)

def password_match(username, password):
    with get_session() as session:
        user = session.query(User).filter_by(username=username).first()
        return user is not None and user.password == password

def get_user_id(username):
    with get_session() as session:
        user = session.query(User).filter_by(username=username).first()
        return user.id if user else None

def get_all_users():
    with get_session() as session:
        return session.query(User).all()

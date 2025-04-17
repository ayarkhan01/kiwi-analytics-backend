from db import get_session
from models.users import User

def password_match(username, password):
    with get_session() as session:
        user = session.query(User).filter_by(username=username).first()
        return user is not None and user.password == password

def get_user_id(username):
    with get_session() as session:
        user = session.query(User).filter_by(username=username).first()
        return user.id if user else None
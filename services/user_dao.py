from db import get_session
from models.users import User

def create_user(username, password):
    """Create a new user with hashed password"""
    with get_session() as session:
        user = User(username=username, password=password)
        session.add(user)
        session.flush()
        session.refresh(user)
        user_id = user.id
        session.expunge(user)
        return user_id

def password_match(username, password):
    """Securely verify password"""
    with get_session() as session:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            return False
        return (user.password, password)

def get_user_id(username):
    """Get user ID by username"""
    with get_session() as session:
        user = session.query(User).filter_by(username=username).first()
        return user.id if user else None
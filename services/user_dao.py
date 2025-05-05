from db import get_session
from models.users import User
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(username, password):
    """Create a new user with hashed password"""
    hashed_password = generate_password_hash(password)
    with get_session() as session:
        user = User(username=username, password=hashed_password)
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
        return check_password_hash(user.password, password)

def get_user_id(username):
    """Get user ID by username"""
    with get_session() as session:
        user = session.query(User).filter_by(username=username).first()
        return user.id if user else None
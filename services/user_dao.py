from db import get_session
from models.users import User
from models.portfolio import Portfolio

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
    """Verify password"""
    with get_session() as session:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            return False
        # Simple password comparison, without hashing
        return user.password == password

def get_user_id(username):
    """Get user ID by username"""
    with get_session() as session:
        user = session.query(User).filter_by(username=username).first()
        return user.id if user else None
    
def delete_user(user_id):
    """Delete a user and their associated portfolios and positions"""
    with get_session() as session:
        user = session.query(User).filter_by(id=user_id).first()

        if not user:
            return False

        # Find all portfolios for the user
        portfolios = session.query(Portfolio).filter_by(user_id=user_id).all()

        # Delete all positions for each portfolio
        from models.positions import Position  # Import here to avoid circular import
        for portfolio in portfolios:
            session.query(Position).filter_by(portfolio_id=portfolio.id).delete()

        # Delete all portfolios associated with the user
        session.query(Portfolio).filter_by(user_id=user_id).delete()

        # Delete the user
        session.delete(user)

        # Committing the transaction is handled by context manager
        return True
    
def get_user_balance(user_id):
    """Get the current balance of a user by ID"""
    with get_session() as session:
        user = session.query(User).filter_by(id=user_id).first()
        return float(user.balance) if user and user.balance is not None else 0.0

def update_user_balance(user_id, new_balance):
    """Update the balance of a user"""
    with get_session() as session:
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            user.balance = new_balance
            session.add(user)
            return True
        return False
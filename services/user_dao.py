from db import get_session
from models.users import User

def create_user(username, password, balance):
    user=User(username=username, password=password, balance=balance)
    with get_session() as session:
        session.add(user)
        session.commit()

def password_match(username, password):
    session = get_session()
    user = session.query(User).filter(User.username==username).first()
    if user is None:
        return False
    if user.password == password:
        print("Password match")
        return True

def get_all():
    session = get_session()
    return session.query(User).all()

def get_active():
    session = get_session()
    return session.query(User).filter(User.is_active==True).all()
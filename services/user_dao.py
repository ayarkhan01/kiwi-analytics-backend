from db import get_session
from models.users import User

def create_user(username, password, balance):
    user=User(username=username, password=password, balance=balance)
    with get_session() as session:
        session.add(user)
        session.commit()

def get_all():
    session = get_session()
    return session.query(User).all()

def get_active():
    session = get_session()
    return session.query(User).filter(User.is_active==True).all()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import get_conn_string
from contextlib import contextmanager

# Base and engine setup
Base = declarative_base()
DB_URI = get_conn_string()
engine = create_engine(DB_URI, echo=False)

# Session factory
SessionLocal = sessionmaker(bind=engine)

# Context-managed session
@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

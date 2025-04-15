import os
from dotenv import load_dotenv

load_dotenv()  # Loads .env into environment

def get_conn_string():
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "3306")
    database = os.getenv("DB_NAME")

    return f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"

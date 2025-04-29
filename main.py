from services.position_dao import get_positions_by_portfolio
from services.user_dao import password_match, get_user_id

admin = input("Enter username: ")
password = input("Enter password: ")
if password_match(admin, password):
    print("Login successful")
    user_id = get_user_id(admin)
    print(f"User ID: {user_id}")
else:
    print("Login failed")


#Market start
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import market_api  # import your new router

app = FastAPI()

# Optional: enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the route
app.include_router(market_api.router, prefix="/api")


#market ends 
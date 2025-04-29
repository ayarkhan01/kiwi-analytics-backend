from fastapi import APIRouter
from services.market_service import fetch_market_data

router = APIRouter()

@router.get("/market")
def get_market_data():
    return fetch_market_data()

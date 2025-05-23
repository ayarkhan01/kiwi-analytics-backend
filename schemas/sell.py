from pydantic import BaseModel

class SellRequest(BaseModel):
    portfolio_id: int
    ticker: str
    quantity: int
    price: float
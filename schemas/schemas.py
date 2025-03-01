from datetime import datetime
from pydantic import BaseModel, ConfigDict


class RequestData(BaseModel):
    browser: str
    url: str

class PricesResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    original_price: str
    discount_price: str
    timestamp: datetime
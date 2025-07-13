from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AlertBase(BaseModel):
    user_email: str
    origin_codes: str
    destination_codes: str
    departure_date_from: str
    departure_date_to: str
    max_price: float
    stay_duration_from: Optional[int] = None
    stay_duration_to: Optional[int] = None

class AlertCreate(AlertBase):
    pass

class Alert(AlertBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
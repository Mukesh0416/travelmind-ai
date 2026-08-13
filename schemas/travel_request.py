from pydantic import BaseModel
from typing import Optional


class TravelRequest(BaseModel):
    user_id: Optional[str] = None
    destination: str
    days: int
    travelers: int = 1
    budget_per_day: float
    interests: Optional[list[str]] = None
    travel_style: Optional[str] = None
    preferences: Optional[dict] = None

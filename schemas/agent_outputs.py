from pydantic import BaseModel
from typing import List, Optional


class Hotel(BaseModel):
    name: str
    price_range: str
    description: str


class Restaurant(BaseModel):
    name: str
    cuisine: str
    cost_for_two: str


class Transportation(BaseModel):
    best_way_to_reach: str
    local_transportation: str
    estimated_cost: str
    travel_tips: str


class PackingItem(BaseModel):
    category: str
    items: List[str]


class DayPlan(BaseModel):
    day: int
    morning_activity: str
    morning_attraction: str
    afternoon_activity: str
    lunch_recommendation: str
    evening_activity: str
    dinner_recommendation: str
    estimated_daily_spending: str
    travel_tips: List[str]
    weather_considerations: str


class Itinerary(BaseModel):
    destination: str
    days: int
    day_plans: List[DayPlan]
    hotel_suggestions: List[str]
    budget_breakdown: str
    overall_travel_tips: List[str]
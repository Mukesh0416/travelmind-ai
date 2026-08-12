from typing import TypedDict, Optional


class TravelState(TypedDict, total=False):
    destination: str
    days: int
    travelers: int
    budget_per_day: float
    interests: list[str]
    travel_style: Optional[str]

    location: dict
    weather: dict
    search_results: list
    budget: dict
    itinerary: dict
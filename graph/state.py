from typing import Optional, TypedDict


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
    places: list
    attractions: list

    budget: dict

    hotels: str
    restaurants: str

    itinerary: str
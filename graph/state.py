from typing import Annotated, Optional, TypedDict


def merge_completed_agents(
    current: Optional[dict],
    new: Optional[dict],
) -> dict:
    """
    Merge partial `completed_agents` updates into the full dict.

    Each agent returns only its own completion flag, e.g.
    `{"completed_agents": {"weather": True}}`. This reducer merges
    those partial updates so parallel agents do not overwrite each other.
    """

    if current is None:
        return dict(new or {})

    merged = dict(current)
    merged.update(new or {})

    return merged


def merge_errors(
    current: Optional[list],
    new: Optional[list],
) -> list:
    """
    Append new error messages to the accumulated error list.
    """

    if current is None:
        return list(new or [])

    return current + list(new or [])


class TravelState(TypedDict, total=False):

    # User inputs
    user_id: str
    destination: str
    days: int
    travelers: int
    budget_per_day: float
    interests: list[str]
    travel_style: str
    preferences: dict

    # Agent outputs
    location: dict
    weather: dict
    search_results: list
    places: list
    attractions: list
    budget: dict
    hotels: list
    restaurants: list
    transportation: dict
    packing_list: list
    itinerary: dict

    # Orchestration
    next_agent: str
    completed_agents: Annotated[dict, merge_completed_agents]
    errors: Annotated[list, merge_errors]

from agents.search_agent import search_agent
from agents.location_agent import location_agent


def itinerary_agent(destination: str, days: int):
    places = search_agent(destination)
    location = location_agent(destination)

    itinerary = {
        "destination": destination,
        "days": days,
        "location": location,
        "places": places,
    }

    return itinerary
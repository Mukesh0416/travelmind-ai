from langchain_groq import ChatGroq

from services.agent_utils import (
    log_agent_complete,
    log_agent_error,
    log_agent_start,
)

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
)


def itinerary_agent(state):
    """
    Create the final day-by-day itinerary.

    Returns a partial state update only. Never mutates the input state.
    """

    log_agent_start("Itinerary")

    destination = state.get("destination", "")

    days = state.get("days", 3)

    travelers = state.get("travelers", 1)

    travel_style = state.get(
        "travel_style",
        "balanced"
    )

    interests = state.get(
        "interests",
        []
    )

    weather = state.get(
        "weather",
        {}
    )

    budget = state.get(
        "budget",
        {}
    )

    attractions = state.get(
        "attractions",
        []
    )

    hotels = state.get(
        "hotels",
        "No hotel recommendations available."
    )

    restaurants = state.get(
        "restaurants",
        "No restaurant recommendations available."
    )

    prompt = f"""
You are an expert travel planner.

Create a {days}-day itinerary for {destination}, India.

Trip information:

Travelers: {travelers}

Travel style: {travel_style}

Interests: {interests}

Weather:

{weather}

Budget:

{budget}

Recommended attractions:

{attractions}

Recommended hotels:

{hotels}

Recommended restaurants:

{restaurants}

Create a realistic day-by-day itinerary.

For each day, include:

Morning:
- Activity
- Attraction

Afternoon:
- Activity
- Lunch recommendation

Evening:
- Activity
- Dinner recommendation

Also include:

- Estimated daily spending
- Travel tips
- Weather considerations

Return the itinerary in a clear format.
"""

    try:

        response = model.invoke(prompt)

        log_agent_complete("Itinerary")

        return {
            "itinerary": response.content,
            "completed_agents": {"itinerary": True},
        }

    except Exception as exc:

        log_agent_error("Itinerary", exc)

        return {
            "itinerary": "Unable to generate itinerary.",
            "completed_agents": {"itinerary": True},
            "errors": [
                f"Itinerary agent failed: {exc}"
            ],
        }
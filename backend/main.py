from fastapi import FastAPI

from graph.travel_graph import run_travel_graph
from schemas.travel_request import TravelRequest
from services.memory import memory

app = FastAPI(title="TravelMind AI")


@app.get("/")
def home():
    return {"message": "TravelMind AI is running!"}


@app.post("/plan")
def plan_trip(request: TravelRequest):
    """
    Run the multi-agent travel planning graph for a given request.

    Returns the full state produced by the supervisor-driven agent team.
    """

    state = {
        "user_id": request.user_id,
        "destination": request.destination,
        "days": request.days,
        "travelers": request.travelers,
        "budget_per_day": request.budget_per_day,
        "interests": request.interests or [],
        "travel_style": request.travel_style or "balanced",
    }

    # Save any new preferences to memory.
    if request.user_id and request.preferences:

        memory.set_preferences(
            request.user_id,
            request.preferences,
        )

    result = run_travel_graph(state=state)

    return result


@app.get("/memory/{user_id}")
def get_user_memory(user_id: str):
    """
    Return the stored preferences and travel history for a user.
    """

    return {
        "user_id": user_id,
        "preferences": memory.get_preferences(user_id),
    }


@app.post("/memory/{user_id}")
def update_user_memory(user_id: str, preferences: dict):
    """
    Merge new preferences into a user's stored memory.
    """

    updated = memory.set_preferences(user_id, preferences)

    return {
        "user_id": user_id,
        "preferences": updated,
    }
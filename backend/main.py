from fastapi import FastAPI

from graph.travel_graph import run_travel_graph
from schemas.travel_request import TravelRequest

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
        "destination": request.destination,
        "days": request.days,
        "travelers": request.travelers,
        "budget_per_day": request.budget_per_day,
        "interests": request.interests or [],
        "travel_style": request.travel_style or "balanced",
    }

    result = run_travel_graph(state=state)

    return result
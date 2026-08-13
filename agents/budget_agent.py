from services.agent_utils import (
    log_agent_complete,
    log_agent_start,
)


def budget_agent(state):
    """
    Calculate the trip budget from user inputs.

    Returns a partial state update only. Never mutates the input state.
    """

    log_agent_start("Budget")

    travelers = state["travelers"]
    days = state["days"]
    budget_per_day = state["budget_per_day"]

    accommodation = budget_per_day * 0.40
    food = budget_per_day * 0.20
    transportation = budget_per_day * 0.15
    activities = budget_per_day * 0.20
    emergency = budget_per_day * 0.05

    log_agent_complete("Budget")

    return {
        "budget": {
            "accommodation": (
                accommodation * days * travelers
            ),
            "food": (
                food * days * travelers
            ),
            "transportation": (
                transportation * days * travelers
            ),
            "activities": (
                activities * days * travelers
            ),
            "emergency": (
                emergency * days * travelers
            ),
            "total_budget": (
                budget_per_day * days * travelers
            ),
        },
        "completed_agents": {"budget": True},
    }
from typing import Dict


def budget_agent(state):

    travelers = state["travelers"]

    days = state["days"]

    budget_per_day = state["budget_per_day"]

    accommodation = budget_per_day * 0.40

    food = budget_per_day * 0.20

    transportation = budget_per_day * 0.15

    activities = budget_per_day * 0.20

    emergency = budget_per_day * 0.05

    state["budget"] = {

        "accommodation": (
            accommodation
            * days
            * travelers
        ),

        "food": (
            food
            * days
            * travelers
        ),

        "transportation": (
            transportation
            * days
            * travelers
        ),

        "activities": (
            activities
            * days
            * travelers
        ),

        "emergency": (
            emergency
            * days
            * travelers
        ),

        "total_budget": (
            budget_per_day
            * days
            * travelers
        )
    }
    
    state["next_agent"] = "accommodation"

    return state
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


def restaurant_agent(state):
    """
    Recommend restaurants for the destination.

    Returns a partial state update only. Never mutates the input state.
    """

    log_agent_start("Restaurant")

    destination = state["destination"]

    budget = state.get("budget", {}).get("total_budget", 0)

    travel_style = state.get(
        "travel_style",
        "balanced"
    )

    prompt = f"""
Suggest 5 restaurants in {destination}, India.

Travel style: {travel_style}

Total trip budget: ₹{budget}

For each restaurant, provide:

- Restaurant name
- Cuisine
- Approximate cost for two people

Return a concise list.
"""

    try:

        response = model.invoke(prompt)

        log_agent_complete("Restaurant")

        return {
            "restaurants": response.content,
            "completed_agents": {"restaurant": True},
        }

    except Exception as exc:

        log_agent_error("Restaurant", exc)

        return {
            "restaurants": "No restaurant recommendations available.",
            "completed_agents": {"restaurant": True},
            "errors": [
                f"Restaurant agent failed: {exc}"
            ],
        }
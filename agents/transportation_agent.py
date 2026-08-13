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


def transportation_agent(state):
    """
    Recommend transportation options for the trip.

    Returns a partial state update only. Never mutates the input state.
    """

    log_agent_start("Transportation")

    destination = state["destination"]

    travelers = state["travelers"]

    budget = state.get("budget", {}).get("total_budget", 0)

    travel_style = state.get(
        "travel_style",
        "balanced"
    )

    prompt = f"""
You are an expert travel planner.

Suggest transportation options for a trip to
{destination}, India.

Travelers: {travelers}

Total budget: ₹{budget}

Travel style: {travel_style}

Provide:

- Best way to reach the destination
- Local transportation
- Estimated transportation cost
- Travel tips

Return a concise response.
"""

    try:

        response = model.invoke(prompt)

        log_agent_complete("Transportation")

        return {
            "transportation": response.content,
            "completed_agents": {"transportation": True},
        }

    except Exception as exc:

        log_agent_error("Transportation", exc)

        return {
            "transportation": "No transportation recommendations available.",
            "completed_agents": {"transportation": True},
            "errors": [
                f"Transportation agent failed: {exc}"
            ],
        }
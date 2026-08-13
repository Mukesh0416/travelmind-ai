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


def accommodation_agent(state):
    """
    Recommend hotels for the destination.

    Returns a partial state update only. Never mutates the input state.
    """

    log_agent_start("Accommodation")

    destination = state["destination"]

    budget = state.get("budget", {}).get("total_budget", 0)

    travelers = state["travelers"]

    prompt = f"""
Suggest 5 hotels in {destination}, India.

Travelers: {travelers}

Total budget: ₹{budget}

Requirements:

- Hotel name
- Price range
- Short description

Return a concise list.
"""

    try:

        response = model.invoke(prompt)

        log_agent_complete("Accommodation")

        return {
            "hotels": response.content,
            "completed_agents": {"accommodation": True},
        }

    except Exception as exc:

        log_agent_error("Accommodation", exc)

        return {
            "hotels": "No hotel recommendations available.",
            "completed_agents": {"accommodation": True},
            "errors": [
                f"Accommodation agent failed: {exc}"
            ],
        }
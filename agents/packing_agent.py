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


def packing_agent(state):
    """
    Create a packing checklist for the trip.

    Returns a partial state update only. Never mutates the input state.
    """

    log_agent_start("Packing")

    destination = state["destination"]

    weather = state.get("weather", {})

    days = state["days"]

    travelers = state["travelers"]

    prompt = f"""
You are an expert travel assistant.

Create a packing checklist.

Destination: {destination}

Trip duration: {days} days

Travelers: {travelers}

Weather:

{weather}

Create a checklist containing:

- Clothing
- Footwear
- Electronics
- Documents
- Health essentials
- Miscellaneous items

Return the result as a checklist.
"""

    try:

        response = model.invoke(prompt)

        log_agent_complete("Packing")

        return {
            "packing_list": response.content,
            "completed_agents": {"packing": True},
        }

    except Exception as exc:

        log_agent_error("Packing", exc)

        return {
            "packing_list": "No packing list available.",
            "completed_agents": {"packing": True},
            "errors": [
                f"Packing agent failed: {exc}"
            ],
        }
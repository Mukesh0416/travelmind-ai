from langchain_groq import ChatGroq
from config import *

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
)


def transportation_agent(state):

    destination = state["destination"]

    travelers = state["travelers"]

    budget = state["budget"]["total_budget"]

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

    response = model.invoke(prompt)

    state["transportation"] = response.content

    state["next_agent"] = "packing"

    return state
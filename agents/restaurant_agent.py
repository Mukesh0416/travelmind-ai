from langchain_groq import ChatGroq
from config import *

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
)


def restaurant_agent(state):

    destination = state["destination"]

    budget = state["budget"]["total_budget"]

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

    response = model.invoke(prompt)

    state["restaurants"] = response.content

    state["next_agent"] = "transportation"

    return state
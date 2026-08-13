from langchain_groq import ChatGroq
from config import *

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
)


def accommodation_agent(state):

    destination = state["destination"]

    budget = state["budget"]["total_budget"]

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

    response = model.invoke(prompt)

    state["hotels"] = response.content

    state["next_agent"] = "restaurant"
    
    return state
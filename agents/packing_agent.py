from langchain_groq import ChatGroq
from config import *

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
)


def packing_agent(state):

    destination = state["destination"]

    weather = state["weather"]

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

    response = model.invoke(prompt)

    state["packing_list"] = response.content

    state["next_agent"] = "itinerary"

    return state
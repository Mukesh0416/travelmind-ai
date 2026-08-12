from langchain_openai import ChatOpenAI
from langgraph.types import Command


def create_supervisor():
    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
    )

    def supervisor(state):

        current_step = state.get("next_agent")

        if current_step == "weather":
            return Command(goto="weather")

        if current_step == "search":
            return Command(goto="search")

        if current_step == "budget":
            return Command(goto="budget")

        if current_step == "end":
            return Command(goto="__end__")

        prompt = f"""
You are the Supervisor Agent of TravelMind AI.

Your job is to decide which specialist agent should work first.

Available agents:
- location
- weather
- search
- budget

Travel request:
Destination: {state.get("destination")}
Days: {state.get("days")}
Travelers: {state.get("travelers")}
Budget per day: {state.get("budget_per_day")}
Interests: {state.get("interests")}
Travel style: {state.get("travel_style")}

Which agent should start?

Return ONLY one word:
location
"""

        response = model.invoke(prompt)

        agent = response.content.strip().lower()

        if agent != "location":
            agent = "location"

        return Command(goto=agent)

    return supervisor
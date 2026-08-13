# # from langchain_groq import ChatGroq
# from langgraph.types import Command
# from config import *

# def create_supervisor():

#     # model = ChatGroq(
#     #     model="llama-3.1-8b-instant",
#     #     temperature=0,
#     # )

#     def supervisor(state):

#         current_step = state.get("next_agent")

#         agent_flow = {

#             "weather": "weather",

#             "search": "search",

#             "budget": "budget",

#             "accommodation": "accommodation",

#             "restaurant": "restaurant",

#             "transportation": "transportation",

#             "packing": "packing",

#             "itinerary": "itinerary",

#             "end": "__end__"
#         }

#         if current_step in agent_flow:

#             return Command(
#                 goto=agent_flow[current_step]
#             )

#         prompt = f"""
# You are the supervisor of a multi-agent travel planning system.

# Available agents:

# - location
# - weather
# - search
# - budget
# - accommodation
# - restaurant
# - transportation
# - packing
# - itinerary

# Travel request:

# Destination: {state.get("destination")}
# Days: {state.get("days")}
# Travelers: {state.get("travelers")}
# Budget per day: {state.get("budget_per_day")}
# Travel style: {state.get("travel_style")}

# Which agent should execute first?

# Return only one word.

# Example:

# location
# """

#         response = model.invoke(prompt)

#         agent = (
#             response.content
#             .strip()
#             .lower()
#         )

#         if agent != "location":

#             agent = "location"

#         return Command(
#             goto=agent
#         )

#     return supervisor

from langgraph.types import Command


def create_supervisor():

    def supervisor(state):

        next_agent = state.get(
            "next_agent",
            "location"
        )

        routes = {

            "location": "location",

            "weather": "weather",

            "search": "search",

            "budget": "budget",

            "accommodation": "accommodation",

            "restaurant": "restaurant",

            "transportation": "transportation",

            "packing": "packing",

            "itinerary": "itinerary",

            "end": "__end__"
        }

        return Command(
            goto=routes.get(
                next_agent,
                "__end__"
            )
        )

    return supervisor
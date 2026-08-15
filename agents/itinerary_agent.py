from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

from schemas.agent_outputs import Itinerary

from services.agent_utils import (
    log_agent_complete,
    log_agent_error,
    log_agent_start,
)

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
)

parser = JsonOutputParser(pydantic_object=Itinerary)

prompt_template = PromptTemplate(
    template="""
You are an expert travel planner.

Create a {days}-day itinerary for {destination}, India.

Trip information:

Travelers: {travelers}

Travel style: {travel_style}

Interests: {interests}

User preferences:

{preferences}

Weather:

{weather}

Budget:

{budget}

Recommended attractions:

{attractions}

Recommended hotels:

{hotels}

Recommended restaurants:

{restaurants}

Return a JSON object with these fields:

- destination: destination name
- days: number of days
- day_plans: array of day plan objects, each with:
  - day: day number
  - morning_activity: morning activity
  - morning_attraction: morning attraction
  - afternoon_activity: afternoon activity
  - lunch_recommendation: lunch recommendation
  - evening_activity: evening activity
  - dinner_recommendation: dinner recommendation
  - estimated_daily_spending: estimated daily spending
  - travel_tips: array of travel tip strings
  - weather_considerations: weather considerations
- hotel_suggestions: array of hotel suggestion strings
- budget_breakdown: budget breakdown string
- overall_travel_tips: array of overall travel tip strings

Return ONLY valid JSON. No markdown, no extra text.

{format_instructions}
""",
    input_variables=[
        "destination",
        "days",
        "travelers",
        "travel_style",
        "interests",
        "weather",
        "budget",
        "attractions",
        "hotels",
        "restaurants",
        "preferences",
    ],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt_template | model | parser


def itinerary_agent(state):
    """
    Create the final day-by-day itinerary.

    Returns a partial state update only. Never mutates the input state.
    """

    log_agent_start("Itinerary")

    destination = state.get("destination", "")

    days = state.get("days", 3)

    travelers = state.get("travelers", 1)

    travel_style = state.get(
        "travel_style",
        "balanced"
    )

    interests = state.get(
        "interests",
        []
    )

    weather = state.get(
        "weather",
        {}
    )

    budget = state.get(
        "budget",
        {}
    )

    attractions = state.get(
        "attractions",
        []
    )

    hotels = state.get(
        "hotels",
        []
    )

    restaurants = state.get(
        "restaurants",
        []
    )

    preferences = state.get(
        "preferences",
        {}
    )

    try:

        itinerary = chain.invoke({
            "destination": destination,
            "days": days,
            "travelers": travelers,
            "travel_style": travel_style,
            "interests": interests,
            "weather": weather,
            "budget": budget,
            "attractions": attractions,
            "hotels": hotels,
            "restaurants": restaurants,
            "preferences": preferences,
        })

        log_agent_complete("Itinerary")

        return {
            "itinerary": itinerary,
            "completed_agents": {"itinerary": True},
        }

    except Exception as exc:

        log_agent_error("Itinerary", exc)

        return {
            "itinerary": {},
            "completed_agents": {"itinerary": True},
            "errors": [
                f"Itinerary agent failed: {exc}"
            ],
        }
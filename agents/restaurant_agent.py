from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from config import GROQ_API_KEY
from schemas.agent_outputs import Restaurant

from services.agent_utils import (
    log_agent_complete,
    log_agent_error,
    log_agent_start,
)

model = ChatGroq(
    api_key=GROQ_API_KEY,
    model="groq/compound-mini",
    temperature=0.3,
)

parser = JsonOutputParser(pydantic_object=Restaurant)

prompt_template = PromptTemplate(
    template="""
Suggest 5 restaurants in {destination}, India.

Travel style: {travel_style}

Total trip budget: ₹{budget}

User restaurant preferences:

{restaurant_preferences}

Return a JSON array of exactly 5 restaurant objects.
Each object must have these fields:

- name: restaurant name
- cuisine: cuisine type
- cost_for_two: approximate cost for two people

Return ONLY valid JSON. No markdown, no extra text.

{format_instructions}
""",
    input_variables=[
        "destination",
        "travel_style",
        "budget",
        "restaurant_preferences",
    ],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt_template | model | parser


def restaurant_agent(state):
    """
    Recommend restaurants for the destination.

    Returns a partial state update only. Never mutates the input state.
    """

    log_agent_start("Restaurant")

    destination = state["destination"]

    budget = state.get("budget", {}).get("total_budget", 0)

    travel_style = state.get(
        "travel_style",
        "balanced"
    )

    try:

        restaurant_preferences = state.get(
            "preferences",
            {},
        ).get("restaurant_preferences", {})

        restaurants = chain.invoke({
            "destination": destination,
            "travel_style": travel_style,
            "budget": budget,
            "restaurant_preferences": restaurant_preferences,
        })

        log_agent_complete("Restaurant")

        return {
            "restaurants": restaurants,
            "completed_agents": {"restaurant": True},
        }

    except Exception as exc:

        log_agent_error("Restaurant", exc)

        return {
            "restaurants": [],
            "completed_agents": {"restaurant": True},
            "errors": [
                f"Restaurant agent failed: {exc}"
            ],
        }
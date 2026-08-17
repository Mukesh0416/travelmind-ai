from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from config import GROQ_API_KEY
from schemas.agent_outputs import Hotel

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

parser = JsonOutputParser(pydantic_object=Hotel)

prompt_template = PromptTemplate(
    template="""
Suggest 5 hotels in {destination}, India.

Travelers: {travelers}

Total budget: ₹{budget}

User hotel preferences:

{hotel_preferences}

Return a JSON array of exactly 5 hotel objects.
Each object must have these fields:

- name: hotel name
- price_range: price range string
- description: short description

Return ONLY valid JSON. No markdown, no extra text.

{format_instructions}
""",
    input_variables=["destination", "travelers", "budget", "hotel_preferences"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt_template | model | parser


def accommodation_agent(state):
    """
    Recommend hotels for the destination.

    Returns a partial state update only. Never mutates the input state.
    """

    log_agent_start("Accommodation")

    destination = state["destination"]

    budget = state.get("budget", {}).get("total_budget", 0)

    travelers = state["travelers"]

    try:

        hotel_preferences = state.get(
            "preferences",
            {},
        ).get("hotel_preferences", {})

        hotels = chain.invoke({
            "destination": destination,
            "travelers": travelers,
            "budget": budget,
            "hotel_preferences": hotel_preferences,
        })

        log_agent_complete("Accommodation")

        return {
            "hotels": hotels,
            "completed_agents": {"accommodation": True},
        }

    except Exception as exc:

        log_agent_error("Accommodation", exc)

        return {
            "hotels": [],
            "completed_agents": {"accommodation": True},
            "errors": [
                f"Accommodation agent failed: {exc}"
            ],
        }
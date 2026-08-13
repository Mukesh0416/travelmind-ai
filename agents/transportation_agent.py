from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

from schemas.agent_outputs import Transportation

from services.agent_utils import (
    log_agent_complete,
    log_agent_error,
    log_agent_start,
)

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
)

parser = JsonOutputParser(pydantic_object=Transportation)

prompt_template = PromptTemplate(
    template="""
You are an expert travel planner.

Suggest transportation options for a trip to
{destination}, India.

Travelers: {travelers}

Total budget: ₹{budget}

Travel style: {travel_style}

Return a JSON object with these fields:

- best_way_to_reach: best way to reach the destination
- local_transportation: local transportation options
- estimated_cost: estimated transportation cost
- travel_tips: travel tips

Return ONLY valid JSON. No markdown, no extra text.

{format_instructions}
""",
    input_variables=["destination", "travelers", "budget", "travel_style"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt_template | model | parser


def transportation_agent(state):
    """
    Recommend transportation options for the trip.

    Returns a partial state update only. Never mutates the input state.
    """

    log_agent_start("Transportation")

    destination = state["destination"]

    travelers = state["travelers"]

    budget = state.get("budget", {}).get("total_budget", 0)

    travel_style = state.get(
        "travel_style",
        "balanced"
    )

    try:

        transportation = chain.invoke({
            "destination": destination,
            "travelers": travelers,
            "budget": budget,
            "travel_style": travel_style,
        })

        log_agent_complete("Transportation")

        return {
            "transportation": transportation,
            "completed_agents": {"transportation": True},
        }

    except Exception as exc:

        log_agent_error("Transportation", exc)

        return {
            "transportation": {},
            "completed_agents": {"transportation": True},
            "errors": [
                f"Transportation agent failed: {exc}"
            ],
        }
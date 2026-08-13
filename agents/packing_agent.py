from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

from schemas.agent_outputs import PackingItem

from services.agent_utils import (
    log_agent_complete,
    log_agent_error,
    log_agent_start,
)

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
)

parser = JsonOutputParser(pydantic_object=PackingItem)

prompt_template = PromptTemplate(
    template="""
You are an expert travel assistant.

Create a packing checklist.

Destination: {destination}

Trip duration: {days} days

Travelers: {travelers}

Weather:

{weather}

Return a JSON array of packing category objects.
Each object must have these fields:

- category: category name (e.g. Clothing, Footwear, Electronics, Documents, Health essentials, Miscellaneous)
- items: list of item strings

Return ONLY valid JSON. No markdown, no extra text.

{format_instructions}
""",
    input_variables=["destination", "days", "travelers", "weather"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt_template | model | parser


def packing_agent(state):
    """
    Create a packing checklist for the trip.

    Returns a partial state update only. Never mutates the input state.
    """

    log_agent_start("Packing")

    destination = state["destination"]

    weather = state.get("weather", {})

    days = state["days"]

    travelers = state["travelers"]

    try:

        packing_list = chain.invoke({
            "destination": destination,
            "days": days,
            "travelers": travelers,
            "weather": weather,
        })

        log_agent_complete("Packing")

        return {
            "packing_list": packing_list,
            "completed_agents": {"packing": True},
        }

    except Exception as exc:

        log_agent_error("Packing", exc)

        return {
            "packing_list": [],
            "completed_agents": {"packing": True},
            "errors": [
                f"Packing agent failed: {exc}"
            ],
        }
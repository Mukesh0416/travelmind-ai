from tools.tavily_tool import search_travel_info
from tools.search_helper import extract_places
from agents.ranking_agent import ranking_agent

from services.agent_utils import (
    log_agent_complete,
    log_agent_error,
    log_agent_start,
)


def search_agent(state):
    """
    Search for tourist attractions in the destination.

    Returns a partial state update only. Never mutates the input state.
    """

    log_agent_start("Search")

    destination = state["destination"]

    query = (
        f"tourist attractions travel guide "
        f"things to do in {destination}, India"
    )

    try:

        results = search_travel_info(query)

        places = extract_places(results)

        ranked_places = ranking_agent(places)

        log_agent_complete("Search")

        return {
            "search_results": results,
            "places": places,
            "attractions": ranked_places,
            "completed_agents": {"search": True},
        }

    except Exception as exc:

        log_agent_error("Search", exc)

        return {
            "search_results": [],
            "places": [],
            "attractions": [],
            "completed_agents": {"search": True},
            "errors": [
                f"Search agent failed: {exc}"
            ],
        }
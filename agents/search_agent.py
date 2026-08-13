from tools.tavily_tool import search_travel_info
from tools.search_helper import extract_places
from agents.ranking_agent import ranking_agent


def search_agent(state):

    destination = state["destination"]

    query = (
        f"tourist attractions travel guide "
        f"things to do in {destination}, India"
    )

    results = search_travel_info(query)

    places = extract_places(results)

    ranked_places = ranking_agent(places)

    state["search_results"] = results

    state["places"] = places

    state["attractions"] = ranked_places

    state["next_agent"] = "budget"

    return state
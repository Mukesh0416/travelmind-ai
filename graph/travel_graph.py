from langgraph.graph import StateGraph, START, END

from graph.state import TravelState
from agents.location_agent import location_agent
from agents.weather_agent import weather_agent
from agents.search_agent import search_agent
from agents.budget_agent import budget_agent


def location_node(state: TravelState):
    result = location_agent(state["destination"])
    return {"location": result}


def weather_node(state: TravelState):
    location = state["location"]

    result = weather_agent(
        location["latitude"],
        location["longitude"],
    )

    return {"weather": result}


def search_node(state: TravelState):
    result = search_agent(state["destination"])
    return {"search_results": result}


def budget_node(state: TravelState):
    result = budget_agent(
        state["budget_per_day"],
        state["days"],
        state["travelers"],
    )

    return {"budget": result}


def create_graph():
    graph = StateGraph(TravelState)

    graph.add_node("location", location_node)
    graph.add_node("weather", weather_node)
    graph.add_node("search", search_node)
    graph.add_node("budget", budget_node)

    graph.add_edge(START, "location")
    graph.add_edge("location", "weather")
    graph.add_edge("weather", "search")
    graph.add_edge("search", "budget")
    graph.add_edge("budget", END)

    return graph.compile()
from langgraph.graph import StateGraph, START
from langgraph.types import Command

from graph.state import TravelState
from agents.location_agent import location_agent
from agents.weather_agent import weather_agent
from agents.search_agent import search_agent
from agents.budget_agent import budget_agent
from agents.supervisor_agent import create_supervisor


def location_node(state: TravelState):
    result = location_agent(state["destination"])
    return {
        "location": result,
        "next_agent": "weather",
    }


def weather_node(state: TravelState):
    location = state["location"]

    result = weather_agent(
        location["latitude"],
        location["longitude"],
    )

    return {
        "weather": result,
        "next_agent": "search",
    }


def search_node(state: TravelState):
    result = search_agent(state["destination"])

    return {
        "search_results": result,
        "next_agent": "budget",
    }


def budget_node(state: TravelState):
    result = budget_agent(
        state["budget_per_day"],
        state["days"],
        state["travelers"],
    )

    return {
        "budget": result,
        "next_agent": "end",
    }


def supervisor_node(state: TravelState):
    supervisor = create_supervisor()

    return supervisor(state)


def create_graph():

    graph = StateGraph(TravelState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("location", location_node)
    graph.add_node("weather", weather_node)
    graph.add_node("search", search_node)
    graph.add_node("budget", budget_node)

    graph.add_edge(START, "supervisor")

    graph.add_edge("location", "weather")
    graph.add_edge("weather", "search")
    graph.add_edge("search", "budget")

    return graph.compile()
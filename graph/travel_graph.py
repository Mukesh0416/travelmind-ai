from langgraph.graph import StateGraph
from langgraph.graph import START, END

from graph.state import TravelState

from agents.supervisor_agent import create_supervisor

from agents.location_agent import location_agent
from agents.weather_agent import weather_agent
from agents.search_agent import search_agent
from agents.budget_agent import budget_agent
from agents.accommodation_agent import accommodation_agent
from agents.restaurant_agent import restaurant_agent
from agents.transportation_agent import transportation_agent
from agents.packing_agent import packing_agent
from agents.itinerary_agent import itinerary_agent


def create_graph():

    graph = StateGraph(TravelState)

    supervisor = create_supervisor()

    graph.add_node(
        "supervisor",
        supervisor
    )

    graph.add_node(
        "location",
        location_agent
    )

    graph.add_node(
        "weather",
        weather_agent
    )

    graph.add_node(
        "search",
        search_agent
    )

    graph.add_node(
        "budget",
        budget_agent
    )

    graph.add_node(
        "accommodation",
        accommodation_agent
    )

    graph.add_node(
        "restaurant",
        restaurant_agent
    )

    graph.add_node(
        "transportation",
        transportation_agent
    )

    graph.add_node(
        "packing",
        packing_agent
    )

    graph.add_node(
        "itinerary",
        itinerary_agent
    )

    graph.add_edge(
        START,
        "supervisor"
    )

    graph.add_edge(
        "location",
        "supervisor"
    )

    graph.add_edge(
        "weather",
        "supervisor"
    )

    graph.add_edge(
        "search",
        "supervisor"
    )

    graph.add_edge(
        "budget",
        "supervisor"
    )

    graph.add_edge(
        "accommodation",
        "supervisor"
    )

    graph.add_edge(
        "restaurant",
        "supervisor"
    )

    graph.add_edge(
        "transportation",
        "supervisor"
    )

    graph.add_edge(
        "packing",
        "supervisor"
    )

    graph.add_edge(
        "itinerary",
        END
    )

    return graph.compile()


travel_graph = create_graph()


def run_travel_graph(destination):

    state = {

        "destination": destination,

        "days": 3,

        "travelers": 2,

        "budget_per_day": 3000,

        "interests": [],

        "travel_style": "balanced",

        "next_agent": "location"
    }

    return travel_graph.invoke(state)
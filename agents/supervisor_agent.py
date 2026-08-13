from langgraph.types import Command

from services.agent_utils import logger

# ---------------------------------------------------------------------------
# Agent dependency graph
# ---------------------------------------------------------------------------
#
# Each agent lists the agents that must complete before it can run.
# Adding a new agent later only requires:
#   1. Registering it in the graph (travel_graph.py)
#   2. Adding its dependencies here
# No supervisor logic changes are needed.

AGENT_DEPENDENCIES = {
    "location": [],
    "weather": ["location"],
    "search": ["location"],
    "budget": [],
    "accommodation": ["budget", "search"],
    "restaurant": ["budget", "search"],
    "transportation": ["location", "weather"],
    "packing": ["weather", "transportation"],
    "itinerary": [
        "weather",
        "search",
        "accommodation",
        "restaurant",
        "transportation",
        "packing",
    ],
}


def create_supervisor():
    """
    Create a supervisor node that dynamically routes to agents.

    The supervisor inspects `completed_agents` in the state, finds every
    agent whose dependencies are satisfied and that has not yet run, and
    returns a `Command` that fans out to all ready agents in parallel.

    When no agent is ready, the supervisor terminates the graph.
    """

    def supervisor(state):

        completed = state.get("completed_agents", {})

        # Find all agents that are ready to run.
        ready_agents = []

        for agent, dependencies in AGENT_DEPENDENCIES.items():

            if completed.get(agent):
                continue

            if all(completed.get(dep) for dep in dependencies):
                ready_agents.append(agent)

        # Nothing left to do -> end the graph.
        if not ready_agents:

            logger.info("[Supervisor] All agents completed. Ending.")

            return Command(goto="__end__")

        # Single agent -> route directly.
        if len(ready_agents) == 1:

            agent = ready_agents[0]

            logger.info(f"[Supervisor] Executing {agent} Agent")

            return Command(goto=agent)

        # Multiple agents -> run in parallel.
        logger.info(
            f"[Supervisor] Executing in parallel: {ready_agents}"
        )

        return Command(goto=ready_agents)

    return supervisor
from tools.osm_tool import search_location

from services.agent_utils import (
    log_agent_complete,
    log_agent_error,
    log_agent_start,
)


def location_agent(state):
    """
    Resolve the destination to geographic coordinates.

    Returns a partial state update only. Never mutates the input state.
    """

    log_agent_start("Location")

    destination = state["destination"]

    try:

        results = search_location(destination)

        if not results:

            log_agent_complete("Location")

            return {
                "location": {
                    "place": destination,
                    "found": False,
                },
                "completed_agents": {"location": True},
                "errors": [
                    f"Location not found for '{destination}'"
                ],
            }

        location = results[0]

        log_agent_complete("Location")

        return {
            "location": {
                "place": destination,
                "found": True,
                "latitude": float(location["lat"]),
                "longitude": float(location["lon"]),
                "display_name": location["display_name"],
            },
            "completed_agents": {"location": True},
        }

    except Exception as exc:

        log_agent_error("Location", exc)

        return {
            "location": {
                "place": destination,
                "found": False,
            },
            "completed_agents": {"location": True},
            "errors": [
                f"Location agent failed: {exc}"
            ],
        }
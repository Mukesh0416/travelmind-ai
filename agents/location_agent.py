from tools.osm_tool import search_location


def location_agent(state):

    destination = state["destination"]

    results = search_location(destination)

    if not results:

        state["location"] = {
            "place": destination,
            "found": False
        }

        state["next_agent"] = "end"

        return state

    location = results[0]

    state["location"] = {
        "place": destination,
        "found": True,
        "latitude": float(location["lat"]),
        "longitude": float(location["lon"]),
        "display_name": location["display_name"]
    }

    state["next_agent"] = "weather"

    return state
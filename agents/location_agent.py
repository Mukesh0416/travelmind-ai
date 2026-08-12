from tools.osm_tool import search_location


def location_agent(place: str):
    results = search_location(place)

    if not results:
        return {
            "place": place,
            "found": False,
        }

    location = results[0]

    return {
        "place": place,
        "found": True,
        "latitude": float(location["lat"]),
        "longitude": float(location["lon"]),
        "display_name": location["display_name"],
    }
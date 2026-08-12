from tools.tavily_tool import search_travel_info


def search_agent(destination: str):
    results = search_travel_info(
        f"best places to visit in {destination}"
    )

    return results
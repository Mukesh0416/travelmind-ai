from tavily import TavilyClient
from config import TAVILY_API_KEY


def search_travel_info(query: str):
    client = TavilyClient(api_key=TAVILY_API_KEY)

    response = client.search(
        query=query,
        search_depth="basic",
        max_results=5,
    )

    return response["results"]
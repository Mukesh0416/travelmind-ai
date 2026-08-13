from tavily import TavilyClient

from config import TAVILY_API_KEY
from services.agent_utils import retry


@retry(max_retries=3, delay=1.0)
def search_travel_info(query: str):
    """
    Search for travel information using Tavily.

    Args:
        query: The search query.

    Returns:
        A list of search result objects from Tavily.

    Raises:
        Exception: On API errors after retries are exhausted.
    """

    client = TavilyClient(api_key=TAVILY_API_KEY)

    response = client.search(
        query=query,
        search_depth="advanced",
        topic="general",
        max_results=5,
    )

    return response["results"]
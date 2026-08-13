import requests

from services.agent_utils import retry


@retry(max_retries=3, delay=1.0)
def search_location(place: str):
    """
    Search for a place using OpenStreetMap Nominatim.

    Args:
        place: The place name to search for.

    Returns:
        A list of location results from Nominatim.

    Raises:
        requests.RequestException: On network or HTTP errors.
    """

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": place,
        "format": "json",
        "limit": 5,
    }

    headers = {
        "User-Agent": "TravelMind-AI/1.0"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()
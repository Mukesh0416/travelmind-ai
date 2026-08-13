import requests

from services.agent_utils import retry


@retry(max_retries=3, delay=1.0)
def get_weather(latitude: float, longitude: float):
    """
    Fetch current weather for a location using Open-Meteo.

    Args:
        latitude: Latitude of the location.
        longitude: Longitude of the location.

    Returns:
        Weather JSON response from Open-Meteo.

    Raises:
        requests.RequestException: On network or HTTP errors.
    """

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    }

    response = requests.get(
        url,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()
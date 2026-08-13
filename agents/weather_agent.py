from tools.weather_tool import get_weather

from services.agent_utils import (
    log_agent_complete,
    log_agent_error,
    log_agent_start,
)


def weather_agent(state):
    """
    Fetch current weather for the resolved destination.

    Returns a partial state update only. Never mutates the input state.
    """

    log_agent_start("Weather")

    location = state.get("location", {})

    if not location.get("found"):

        log_agent_complete("Weather")

        return {
            "weather": {},
            "completed_agents": {"weather": True},
            "errors": [
                "Weather agent skipped: location not resolved"
            ],
        }

    latitude = location["latitude"]
    longitude = location["longitude"]

    try:

        weather = get_weather(latitude, longitude)

        log_agent_complete("Weather")

        return {
            "weather": {
                "temperature": weather["current"]["temperature_2m"],
                "humidity": weather["current"]["relative_humidity_2m"],
                "wind_speed": weather["current"]["wind_speed_10m"],
            },
            "completed_agents": {"weather": True},
        }

    except Exception as exc:

        log_agent_error("Weather", exc)

        return {
            "weather": {},
            "completed_agents": {"weather": True},
            "errors": [
                f"Weather agent failed: {exc}"
            ],
        }
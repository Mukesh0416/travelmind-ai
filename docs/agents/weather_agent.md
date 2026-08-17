# Weather Agent

## Purpose

The **Weather Agent** fetches current weather conditions (temperature, humidity, wind speed) for the resolved destination using the Open-Meteo API. It runs after the Location Agent and provides weather data for the Packing and Itinerary agents.

## Inputs

| Field | Type | Description |
|-------|------|-------------|
| `location.latitude` | `float` | Latitude of the destination |
| `location.longitude` | `float` | Longitude of the destination |
| `location.found` | `bool` | Whether the location was resolved |

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| `weather.temperature` | `float` | Current temperature in °C |
| `weather.humidity` | `float` | Relative humidity percentage |
| `weather.wind_speed` | `float` | Wind speed in km/h |
| `completed_agents.weather` | `bool` | Set to `True` when the agent completes |
| `errors` | `list` | Error messages if the agent fails |

## External APIs

- **Open-Meteo** — Free weather API
  - Endpoint: `https://api.open-meteo.com/v1/forecast`
  - Parameters: `latitude`, `longitude`, `current=temperature_2m,relative_humidity_2m,wind_speed_10m`
  - Cost: Free, no API key required

## Dependencies

- **Location Agent** — Requires the destination to be resolved to coordinates.

## Implementation

**File:** `agents/weather_agent.py`

```python
def weather_agent(state):
    """
    Fetch current weather for the resolved destination.
    Returns a partial state update only. Never mutates the input state.
    """
```

**Tool:** `tools/weather_tool.py`

```python
@retry(max_retries=3, delay=1.0)
def get_weather(latitude: float, longitude: float):
    """
    Fetch current weather for a location using Open-Meteo.
    """
```

## Error Handling

- If the location was not resolved, the agent skips and adds an error message.
- If the API call fails, the agent catches the exception, logs it, and returns an empty weather dict.
- The agent uses the `retry` decorator (3 attempts with 1-second delay) for transient failures.

## Downstream Agents

- **Packing Agent** — Uses weather data to generate the packing checklist.
- **Itinerary Agent** — Uses weather data for weather considerations in the itinerary.
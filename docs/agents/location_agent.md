# Location Agent

## Purpose

The **Location Agent** resolves a destination name to geographic coordinates (latitude and longitude) using the OpenStreetMap Nominatim API. It is the first agent to run in the travel planning workflow and provides the geographic foundation for the Weather, Search, and Transportation agents.

## Inputs

| Field | Type | Description |
|-------|------|-------------|
| `destination` | `str` | The destination name entered by the user (e.g., "Manali") |

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| `location.place` | `str` | The destination name |
| `location.found` | `bool` | Whether the location was successfully resolved |
| `location.latitude` | `float` | Latitude of the destination (if found) |
| `location.longitude` | `float` | Longitude of the destination (if found) |
| `location.display_name` | `str` | Full display name from OpenStreetMap |
| `completed_agents.location` | `bool` | Set to `True` when the agent completes |
| `errors` | `list` | Error messages if the agent fails |

## External APIs

- **OpenStreetMap Nominatim** — Free geocoding API
  - Endpoint: `https://nominatim.openstreetmap.org/search`
  - Parameters: `q` (place name), `format=json`, `limit=5`
  - Rate limit: 1 request per second (per Nominatim policy)

## Dependencies

- **None** — This agent has no dependencies and runs first.

## Implementation

**File:** `agents/location_agent.py`

```python
def location_agent(state):
    """
    Resolve the destination to geographic coordinates.
    Returns a partial state update only. Never mutates the input state.
    """
```

**Tool:** `tools/osm_tool.py`

```python
@retry(max_retries=3, delay=1.0)
def search_location(place: str):
    """
    Search for a place using OpenStreetMap Nominatim.
    """
```

## Error Handling

- If the location is not found, the agent returns `found: False` and adds an error message.
- If the API call fails, the agent catches the exception, logs it, and returns `found: False`.
- The agent uses the `retry` decorator (3 attempts with 1-second delay) for transient failures.

## Downstream Agents

- **Weather Agent** — Uses the resolved coordinates to fetch weather.
- **Search Agent** — Uses the destination name for attraction search.
- **Transportation Agent** — Uses the destination for transport recommendations.
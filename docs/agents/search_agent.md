# Search Agent

## Purpose

The **Search Agent** searches for tourist attractions and travel information for the destination using the Tavily search API. It runs after the Location Agent and provides attraction recommendations for the Itinerary Agent.

## Inputs

| Field | Type | Description |
|-------|------|-------------|
| `destination` | `str` | The destination name entered by the user |

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| `search_results` | `list` | Raw search results from Tavily |
| `places` | `list` | Extracted place names from search results |
| `attractions` | `list` | Ranked attraction names |
| `completed_agents.search` | `bool` | Set to `True` when the agent completes |
| `errors` | `list` | Error messages if the agent fails |

## External APIs

- **Tavily** — Search API for travel information
  - Endpoint: Tavily search endpoint
  - Parameters: `query`, `search_depth=advanced`, `topic=general`, `max_results=5`
  - Cost: Free tier available (requires API key)

## Dependencies

- **Location Agent** — Requires the destination to be resolved.

## Implementation

**File:** `agents/search_agent.py`

```python
def search_agent(state):
    """
    Search for tourist attractions in the destination.
    Returns a partial state update only. Never mutates the input state.
    """
```

**Tool:** `tools/tavily_tool.py`

```python
@retry(max_retries=3, delay=1.0)
def search_travel_info(query: str):
    """
    Search for travel information using Tavily.
    """
```

**Helper:** `tools/search_helper.py`

```python
def extract_places(search_results):
    """
    Extract place names from search results.
    """
```

## Ranking

The Search Agent uses the **Ranking Agent** (`agents/ranking_agent.py`) to sort attractions by popularity:

```python
POPULAR_ATTRACTIONS = {
    "Solang Valley": 10,
    "Rohtang Pass": 9,
    "Hadimba Temple": 8,
    "Old Manali": 8,
    "Manu Temple": 7,
    "Van Vihar": 6,
    "Beas River": 6,
}
```

## Error Handling

- If the API call fails, the agent catches the exception, logs it, and returns empty lists.
- The agent uses the `retry` decorator (3 attempts with 1-second delay) for transient failures.

## Downstream Agents

- **Accommodation Agent** — Uses search results for hotel recommendations.
- **Restaurant Agent** — Uses search results for restaurant recommendations.
- **Itinerary Agent** — Uses ranked attractions for the day-by-day plan.
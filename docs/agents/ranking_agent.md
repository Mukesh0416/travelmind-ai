# Ranking Agent

## Purpose

The **Ranking Agent** ranks tourist attractions by popularity. It is a helper agent used by the Search Agent to sort extracted places based on a predefined popularity score.

## Inputs

| Field | Type | Description |
|-------|------|-------------|
| `attractions` | `list` | List of attraction names extracted from search results |

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| `ranked` | `list` | Attraction names sorted by popularity (highest first) |

## External APIs

- **None** — This agent uses a predefined popularity mapping.

## Dependencies

- **Search Agent** — The Ranking Agent is called by the Search Agent.

## Implementation

**File:** `agents/ranking_agent.py`

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

def ranking_agent(attractions):
    ranked = sorted(
        attractions,
        key=lambda x: POPULAR_ATTRACTIONS.get(x, 0),
        reverse=True,
    )
    return ranked
```

## Popularity Scores

| Attraction | Score |
|------------|-------|
| Solang Valley | 10 |
| Rohtang Pass | 9 |
| Hadimba Temple | 8 |
| Old Manali | 8 |
| Manu Temple | 7 |
| Van Vihar | 6 |
| Beas River | 6 |
| *Unknown* | 0 (default) |

## Error Handling

- This agent performs pure sorting and does not require error handling.

## Downstream Agents

- **Search Agent** — Uses the ranked attractions for the itinerary.
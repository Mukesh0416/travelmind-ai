# Restaurant Agent

## Purpose

The **Restaurant Agent** recommends restaurants for the destination using the Groq LLM. It runs after the Budget and Search agents complete and provides restaurant recommendations for the Itinerary Agent.

## Inputs

| Field | Type | Description |
|-------|------|-------------|
| `destination` | `str` | The destination name entered by the user |
| `travel_style` | `str` | User travel style (balanced, luxury, budget, adventure) |
| `budget.total_budget` | `float` | Total trip budget |
| `preferences.restaurant_preferences` | `dict` | User restaurant preferences (optional) |

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| `restaurants` | `list` | List of restaurant objects with name, cuisine, cost_for_two |
| `completed_agents.restaurant` | `bool` | Set to `True` when the agent completes |
| `errors` | `list` | Error messages if the agent fails |

## Restaurant Object Schema

```python
class Restaurant(BaseModel):
    name: str
    cuisine: str
    cost_for_two: str
```

## External APIs

- **Groq** — LLM API for restaurant recommendations
  - Model: `groq/compound-mini`
  - Temperature: 0.3
  - Cost: Free tier available (requires API key)

## Dependencies

- **Budget Agent** — Requires the trip budget for cost-appropriate recommendations.
- **Search Agent** — Requires search results for destination context.

## Implementation

**File:** `agents/restaurant_agent.py`

```python
model = ChatGroq(
    api_key=GROQ_API_KEY,
    model="groq/compound-mini",
    temperature=0.3,
)

chain = prompt_template | model | parser

def restaurant_agent(state):
    """
    Recommend restaurants for the destination.
    Returns a partial state update only. Never mutates the input state.
    """
```

## Prompt Template

The agent prompts the LLM to suggest 5 restaurants in the destination with:

- `destination` — The trip destination
- `travel_style` — User's travel style
- `budget` — Total trip budget
- `restaurant_preferences` — User restaurant preferences

The output is parsed as a JSON array using the `Restaurant` Pydantic model.

## Error Handling

- If the LLM call fails, the agent catches the exception, logs it, and returns an empty restaurants list.
- Invalid JSON from the LLM is handled by the `JsonOutputParser`.

## Downstream Agents

- **Itinerary Agent** — Uses restaurant recommendations for the final itinerary.
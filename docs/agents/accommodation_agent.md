# Accommodation Agent

## Purpose

The **Accommodation Agent** recommends hotels for the destination using the Groq LLM. It runs after the Budget and Search agents complete and provides hotel recommendations for the Itinerary Agent.

## Inputs

| Field | Type | Description |
|-------|------|-------------|
| `destination` | `str` | The destination name entered by the user |
| `travelers` | `int` | Number of travelers |
| `budget.total_budget` | `float` | Total trip budget |
| `preferences.hotel_preferences` | `dict` | User hotel preferences (optional) |

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| `hotels` | `list` | List of hotel objects with name, price_range, description |
| `completed_agents.accommodation` | `bool` | Set to `True` when the agent completes |
| `errors` | `list` | Error messages if the agent fails |

## Hotel Object Schema

```python
class Hotel(BaseModel):
    name: str
    price_range: str
    description: str
```

## External APIs

- **Groq** — LLM API for hotel recommendations
  - Model: `groq/compound-mini`
  - Temperature: 0.3
  - Cost: Free tier available (requires API key)

## Dependencies

- **Budget Agent** — Requires the trip budget for price-appropriate recommendations.
- **Search Agent** — Requires search results for destination context.

## Implementation

**File:** `agents/accommodation_agent.py`

```python
model = ChatGroq(
    api_key=GROQ_API_KEY,
    model="groq/compound-mini",
    temperature=0.3,
)

chain = prompt_template | model | parser

def accommodation_agent(state):
    """
    Recommend hotels for the destination.
    Returns a partial state update only. Never mutates the input state.
    """
```

## Prompt Template

The agent prompts the LLM to suggest 5 hotels in the destination with:

- `destination` — The trip destination
- `travelers` — Number of travelers
- `budget` — Total trip budget
- `hotel_preferences` — User hotel preferences

The output is parsed as a JSON array using the `Hotel` Pydantic model.

## Error Handling

- If the LLM call fails, the agent catches the exception, logs it, and returns an empty hotels list.
- Invalid JSON from the LLM is handled by the `JsonOutputParser`.

## Downstream Agents

- **Itinerary Agent** — Uses hotel recommendations for the final itinerary.
# Transportation Agent

## Purpose

The **Transportation Agent** recommends transportation options for reaching the destination and getting around locally using the Groq LLM. It runs after the Location and Weather agents complete and provides transport recommendations for the Packing and Itinerary agents.

## Inputs

| Field | Type | Description |
|-------|------|-------------|
| `destination` | `str` | The destination name entered by the user |
| `travelers` | `int` | Number of travelers |
| `budget.total_budget` | `float` | Total trip budget |
| `travel_style` | `str` | User travel style (balanced, luxury, budget, adventure) |

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| `transportation.best_way_to_reach` | `str` | Best way to reach the destination |
| `transportation.local_transportation` | `str` | Local transportation options |
| `transportation.estimated_cost` | `str` | Estimated transportation cost |
| `transportation.travel_tips` | `str` | Travel tips |
| `completed_agents.transportation` | `bool` | Set to `True` when the agent completes |
| `errors` | `list` | Error messages if the agent fails |

## Transportation Object Schema

```python
class Transportation(BaseModel):
    best_way_to_reach: str
    local_transportation: str
    estimated_cost: str
    travel_tips: str
```

## External APIs

- **Groq** — LLM API for transportation recommendations
  - Model: `groq/compound-mini`
  - Temperature: 0.3
  - Cost: Free tier available (requires API key)

## Dependencies

- **Location Agent** — Requires the destination to be resolved.
- **Weather Agent** — Uses weather data for travel planning context.

## Implementation

**File:** `agents/transportation_agent.py`

```python
model = ChatGroq(
    api_key=GROQ_API_KEY,
    model="groq/compound-mini",
    temperature=0.3,
)

chain = prompt_template | model | parser

def transportation_agent(state):
    """
    Recommend transportation options for the trip.
    Returns a partial state update only. Never mutates the input state.
    """
```

## Prompt Template

The agent prompts the LLM to suggest transportation options with:

- `destination` — The trip destination
- `travelers` — Number of travelers
- `budget` — Total trip budget
- `travel_style` — User's travel style

The output is parsed as a JSON object using the `Transportation` Pydantic model.

## Error Handling

- If the LLM call fails, the agent catches the exception, logs it, and returns an empty transportation dict.
- Invalid JSON from the LLM is handled by the `JsonOutputParser`.

## Downstream Agents

- **Packing Agent** — Uses transportation context for packing recommendations.
- **Itinerary Agent** — Uses transport options for the final itinerary.
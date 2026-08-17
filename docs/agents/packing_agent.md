# Packing Agent

## Purpose

The **Packing Agent** generates a packing checklist for the trip using the Groq LLM. It runs after the Weather and Transportation agents complete and provides the packing list for the Itinerary Agent.

## Inputs

| Field | Type | Description |
|-------|------|-------------|
| `destination` | `str` | The destination name entered by the user |
| `days` | `int` | Number of trip days |
| `travelers` | `int` | Number of travelers |
| `weather` | `dict` | Current weather data for the destination |

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| `packing_list` | `list` | List of packing category objects with category and items |
| `completed_agents.packing` | `bool` | Set to `True` when the agent completes |
| `errors` | `list` | Error messages if the agent fails |

## PackingItem Object Schema

```python
class PackingItem(BaseModel):
    category: str
    items: List[str]
```

Example categories: Clothing, Footwear, Electronics, Documents, Health essentials, Miscellaneous.

## External APIs

- **Groq** — LLM API for packing checklist generation
  - Model: `groq/compound-mini`
  - Temperature: 0.3
  - Cost: Free tier available (requires API key)

## Dependencies

- **Weather Agent** — Requires weather data to adapt the packing list.
- **Transportation Agent** — Uses transportation context for packing recommendations.

## Implementation

**File:** `agents/packing_agent.py`

```python
model = ChatGroq(
    api_key=GROQ_API_KEY,
    model="groq/compound-mini",
    temperature=0.3,
)

chain = prompt_template | model | parser

def packing_agent(state):
    """
    Create a packing checklist for the trip.
    Returns a partial state update only. Never mutates the input state.
    """
```

## Prompt Template

The agent prompts the LLM to create a packing checklist with:

- `destination` — The trip destination
- `days` — Number of trip days
- `travelers` — Number of travelers
- `weather` — Current weather conditions

The output is parsed as a JSON array using the `PackingItem` Pydantic model.

## Error Handling

- If the LLM call fails, the agent catches the exception, logs it, and returns an empty packing list.
- Invalid JSON from the LLM is handled by the `JsonOutputParser`.

## Downstream Agents

- **Itinerary Agent** — Uses the packing list for the final itinerary.
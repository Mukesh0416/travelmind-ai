# Itinerary Agent

## Purpose

The **Itinerary Agent** creates the final day-by-day itinerary for the trip using the Groq LLM. It runs last, after all other agents complete, and produces the comprehensive trip plan that is displayed to the user.

## Inputs

| Field | Type | Description |
|-------|------|-------------|
| `destination` | `str` | The destination name entered by the user |
| `days` | `int` | Number of trip days |
| `travelers` | `int` | Number of travelers |
| `travel_style` | `str` | User travel style |
| `interests` | `list` | User interests |
| `weather` | `dict` | Current weather data |
| `budget` | `dict` | Budget breakdown |
| `attractions` | `list` | Ranked attractions |
| `hotels` | `list` | Hotel recommendations |
| `restaurants` | `list` | Restaurant recommendations |
| `preferences` | `dict` | User preferences from memory |

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| `itinerary.destination` | `str` | Destination name |
| `itinerary.days` | `int` | Number of days |
| `itinerary.day_plans` | `list` | Day-by-day plan objects |
| `itinerary.hotel_suggestions` | `list` | Hotel suggestion strings |
| `itinerary.budget_breakdown` | `str` | Budget breakdown string |
| `itinerary.overall_travel_tips` | `list` | Overall travel tip strings |
| `completed_agents.itinerary` | `bool` | Set to `True` when the agent completes |
| `errors` | `list` | Error messages if the agent fails |

## Itinerary Object Schema

```python
class DayPlan(BaseModel):
    day: int
    morning_activity: str
    morning_attraction: str
    afternoon_activity: str
    lunch_recommendation: str
    evening_activity: str
    dinner_recommendation: str
    estimated_daily_spending: str
    travel_tips: List[str]
    weather_considerations: str

class Itinerary(BaseModel):
    destination: str
    days: int
    day_plans: List[DayPlan]
    hotel_suggestions: List[str]
    budget_breakdown: str
    overall_travel_tips: List[str]
```

## External APIs

- **Groq** — LLM API for itinerary generation
  - Model: `groq/compound-mini`
  - Temperature: 0.3
  - Cost: Free tier available (requires API key)

## Dependencies

- **Weather Agent** — For weather considerations in the itinerary.
- **Search Agent** — For ranked attractions.
- **Accommodation Agent** — For hotel suggestions.
- **Restaurant Agent** — For dining recommendations.
- **Transportation Agent** — For transport context.
- **Packing Agent** — For packing context.

## Implementation

**File:** `agents/itinerary_agent.py`

```python
model = ChatGroq(
    api_key=GROQ_API_KEY,
    model="groq/compound-mini",
    temperature=0.3,
)

chain = prompt_template | model | parser

def itinerary_agent(state):
    """
    Create the final day-by-day itinerary.
    Returns a partial state update only. Never mutates the input state.
    """
```

## Prompt Template

The agent prompts the LLM to create a day-by-day itinerary with:

- `destination` — Trip destination
- `days` — Number of trip days
- `travelers` — Number of travelers
- `travel_style` — User's travel style
- `interests` — User interests
- `weather` — Current weather conditions
- `budget` — Budget breakdown
- `attractions` — Ranked tourist attractions
- `hotels` — Recommended hotels
- `restaurants` — Recommended restaurants
- `preferences` — User preferences

The output is parsed as a JSON object using the `Itinerary` Pydantic model.

## Error Handling

- If the LLM call fails, the agent catches the exception, logs it, and returns an empty itinerary dict.
- Since this is the final agent, the graph terminates regardless of whether the itinerary was generated.

## Final Output

The Itinerary Agent is the **last node** in the graph. When it completes, the supervisor routes to `END`, and the final state is returned to the caller.
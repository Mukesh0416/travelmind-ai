# Budget Agent

## Purpose

The **Budget Agent** calculates the trip budget allocation based on user inputs (daily budget, number of days, number of travelers). It runs in parallel with the Location Agent as one of the first agents and provides the budget breakdown for Accommodation, Restaurant, Transportation, and Itinerary agents.

## Inputs

| Field | Type | Description |
|-------|------|-------------|
| `travelers` | `int` | Number of travelers |
| `days` | `int` | Number of trip days |
| `budget_per_day` | `float` | Daily budget per person |

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| `budget.accommodation` | `float` | Budget allocated for accommodation (40%) |
| `budget.food` | `float` | Budget allocated for food (20%) |
| `budget.transportation` | `float` | Budget allocated for transportation (15%) |
| `budget.activities` | `float` | Budget allocated for activities (20%) |
| `budget.emergency` | `float` | Emergency buffer (5%) |
| `budget.total_budget` | `float` | Total trip budget |
| `completed_agents.budget` | `bool` | Set to `True` when the agent completes |

## External APIs

- **None** — This agent performs pure calculation.

## Dependencies

- **None** — This agent has no dependencies and runs first.

## Implementation

**File:** `agents/budget_agent.py`

```python
def budget_agent(state):
    """
    Calculate the trip budget from user inputs.
    Returns a partial state update only. Never mutates the input state.
    """
```

## Budget Allocation

| Category | Percentage | Formula |
|----------|-----------|---------|
| Accommodation | 40% | `budget_per_day * 0.40 * days * travelers` |
| Food | 20% | `budget_per_day * 0.20 * days * travelers` |
| Transportation | 15% | `budget_per_day * 0.15 * days * travelers` |
| Activities | 20% | `budget_per_day * 0.20 * days * travelers` |
| Emergency | 5% | `budget_per_day * 0.05 * days * travelers` |
| **Total** | **100%** | `budget_per_day * days * travelers` |

## Error Handling

- This agent performs only arithmetic operations and does not require external API calls; therefore, no error handling is needed beyond the standard agent execution.

## Downstream Agents

- **Accommodation Agent** — Uses the total budget for hotel recommendations.
- **Restaurant Agent** — Uses the total budget for restaurant recommendations.
- **Transportation Agent** — Uses the total budget for transport recommendations.
- **Itinerary Agent** — Uses the budget breakdown for the final itinerary.
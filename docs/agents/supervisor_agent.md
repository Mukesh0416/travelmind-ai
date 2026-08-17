# Supervisor Agent

## Purpose

The **Supervisor Agent** is the central orchestration layer of the TravelMind AI multi-agent system. It dynamically routes to agents based on a dependency graph, enabling parallel execution and ensuring the correct execution order. It is not a "worker" agent — it is the **brain** that coordinates all other agents.

## Inputs

| Field | Type | Description |
|-------|------|-------------|
| `completed_agents` | `dict` | Tracks which agents have completed (`True`/`False` per agent) |

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| `Command(goto=agent)` | `Command` | Routes to a single agent |
| `Command(goto=[agents])` | `Command` | Routes to multiple agents in parallel |
| `Command(goto="__end__")` | `Command` | Terminates the graph when all agents are complete |

## External APIs

- **None** — The supervisor performs pure orchestration logic.

## Dependencies

- **None** — The supervisor is the entry point of the graph.

## Implementation

**File:** `agents/supervisor_agent.py`

```python
AGENT_DEPENDENCIES = {
    "location": [],
    "weather": ["location"],
    "search": ["location"],
    "budget": [],
    "accommodation": ["budget", "search"],
    "restaurant": ["budget", "search"],
    "transportation": ["location", "weather"],
    "packing": ["weather", "transportation"],
    "itinerary": [
        "weather",
        "search",
        "accommodation",
        "restaurant",
        "transportation",
        "packing",
    ],
}

def create_supervisor():
    """
    Create a supervisor node that dynamically routes to agents.
    """
```

## How It Works

1. **Inspect State** — The supervisor reads the `completed_agents` dict from the state.
2. **Find Ready Agents** — It iterates through `AGENT_DEPENDENCIES` and finds every agent whose dependencies are all satisfied and that has not yet run.
3. **Route**:
   - **No ready agents** → `Command(goto="__end__")` — the graph terminates.
   - **One ready agent** → `Command(goto=agent)` — routes to that single agent.
   - **Multiple ready agents** → `Command(goto=[agents])` — routes to all ready agents **in parallel**.
4. **Repeat** — After each agent completes, control returns to the supervisor, which repeats the process.

## Agent Dependency Graph

| Agent | Dependencies |
|-------|-------------|
| Location | None |
| Budget | None |
| Weather | Location |
| Search | Location |
| Accommodation | Budget, Search |
| Restaurant | Budget, Search |
| Transportation | Location, Weather |
| Packing | Weather, Transportation |
| Itinerary | Weather, Search, Accommodation, Restaurant, Transportation, Packing |

## Key Features

- **Dynamic Routing** — No hardcoded execution sequence; routing is based on state.
- **Parallel Execution** — Independent agents run simultaneously.
- **Termination Guarantee** — The graph always terminates when all agents complete.
- **Extensibility** — Adding a new agent only requires registering it in the graph and adding its dependencies.

## Error Handling

- The supervisor itself does not perform error-prone operations.
- If an agent fails, it still marks itself as `completed` in the state, so the supervisor can continue routing.
- Errors are accumulated in the state's `errors` list for the caller to inspect.
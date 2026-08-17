# Agent Documentation

This directory contains documentation for every agent in the TravelMind AI multi-agent system.

## Agents

| Agent | File | Purpose |
|-------|------|---------|
| [Supervisor Agent](supervisor_agent.md) | `agents/supervisor_agent.py` | Orchestrates all agents dynamically |
| [Location Agent](location_agent.md) | `agents/location_agent.py` | Resolves destination to coordinates |
| [Weather Agent](weather_agent.md) | `agents/weather_agent.py` | Fetches current weather |
| [Search Agent](search_agent.md) | `agents/search_agent.py` | Searches for tourist attractions |
| [Budget Agent](budget_agent.md) | `agents/budget_agent.py` | Calculates trip budget |
| [Accommodation Agent](accommodation_agent.md) | `agents/accommodation_agent.py` | Recommends hotels |
| [Restaurant Agent](restaurant_agent.md) | `agents/restaurant_agent.py` | Recommends restaurants |
| [Transportation Agent](transportation_agent.md) | `agents/transportation_agent.py` | Recommends transport options |
| [Packing Agent](packing_agent.md) | `agents/packing_agent.py` | Generates packing checklist |
| [Itinerary Agent](itinerary_agent.md) | `agents/itinerary_agent.py` | Creates day-by-day itinerary |
| [Ranking Agent](ranking_agent.md) | `agents/ranking_agent.py` | Ranks attractions by popularity |

## Execution Order

```text
START
 ↓
Supervisor
 ↓
Location Agent + Budget Agent (parallel)
 ↓
Supervisor
 ↓
Weather Agent + Search Agent (parallel)
 ↓
Supervisor
 ↓
Accommodation + Restaurant + Transportation (parallel)
 ↓
Supervisor
 ↓
Packing Agent
 ↓
Supervisor
 ↓
Itinerary Agent
 ↓
END
# TravelMind AI - Architecture Diagram

```mermaid
graph TD
    subgraph "User Layer"
        U[User]
    end

    subgraph "Frontend Layer"
        SF[Streamlit Frontend<br/>ui/app.py]
    end

    subgraph "Orchestration Layer"
        LS[LangGraph Supervisor<br/>graph/travel_graph.py]
    end

    subgraph "Multi-Agent Workflow"
        LA[Location Agent<br/>agents/location_agent.py]
        WA[Weather Agent<br/>agents/weather_agent.py]
        SA[Search Agent<br/>agents/search_agent.py]
        BA[Budget Agent<br/>agents/budget_agent.py]
        AA[Accommodation Agent<br/>agents/accommodation_agent.py]
        RA[Restaurant Agent<br/>agents/restaurant_agent.py]
        TA[Transportation Agent<br/>agents/transportation_agent.py]
        PA[Packing Agent<br/>agents/packing_agent.py]
        IA[Itinerary Agent<br/>agents/itinerary_agent.py]
    end

    subgraph "Memory Layer"
        MEM[Persistent Memory<br/>memory/memory.py<br/>SQLite]
    end

    subgraph "External APIs"
        OSM[OpenStreetMap<br/>Nominatim API]
        OM[Open-Meteo<br/>Weather API]
        TV[Tavily<br/>Search API]
        GQ[Groq<br/>LLM API]
    end

    U -->|"User Input"| SF
    SF -->|"Trip Request"| LS
    LS -->|"Route & Orchestrate"| LA
    LS -->|"Route & Orchestrate"| WA
    LS -->|"Route & Orchestrate"| SA
    LS -->|"Route & Orchestrate"| BA
    LS -->|"Route & Orchestrate"| AA
    LS -->|"Route & Orchestrate"| RA
    LS -->|"Route & Orchestrate"| TA
    LS -->|"Route & Orchestrate"| PA
    LS -->|"Route & Orchestrate"| IA

    LA -->|"Geographic Coordinates"| OSM
    WA -->|"Weather Data"| OM
    SA -->|"Search Results"| TV
    AA -->|"Hotel Recommendations"| GQ
    RA -->|"Restaurant Recommendations"| GQ
    TA -->|"Transportation Options"| GQ
    PA -->|"Packing List"| GQ
    IA -->|"Itinerary"| GQ

    LA -->|"Save/Load"| MEM
    WA -->|"Save/Load"| MEM
    SA -->|"Save/Load"| MEM
    BA -->|"Save/Load"| MEM
    AA -->|"Save/Load"| MEM
    RA -->|"Save/Load"| MEM
    TA -->|"Save/Load"| MEM
    PA -->|"Save/Load"| MEM
    IA -->|"Save/Load"| MEM

    IA -->|"Final Itinerary"| SF
    SF -->|"Display Results"| U
```

## Component Description

| Component | Description |
|-----------|-------------|
| **User** | The end user who interacts with the application |
| **Streamlit Frontend** | Web-based UI for trip planning, travel history, and user preferences |
| **LangGraph Supervisor** | Orchestration layer that routes agents based on dependencies |
| **Location Agent** | Resolves destination to geographic coordinates via OpenStreetMap |
| **Weather Agent** | Fetches current weather via Open-Meteo |
| **Search Agent** | Searches for tourist attractions via Tavily |
| **Budget Agent** | Calculates trip budget allocation |
| **Accommodation Agent** | Recommends hotels via Groq LLM |
| **Restaurant Agent** | Recommends restaurants via Groq LLM |
| **Transportation Agent** | Recommends transportation options via Groq LLM |
| **Packing Agent** | Generates packing checklist via Groq LLM |
| **Itinerary Agent** | Creates day-by-day itinerary via Groq LLM |
| **Memory Layer** | SQLite-backed persistent storage for user preferences and travel history |
| **OpenStreetMap** | Free geocoding API for location resolution |
| **Open-Meteo** | Free weather API |
| **Tavily** | Search API for travel information |
| **Groq** | LLM API for AI-powered recommendations |
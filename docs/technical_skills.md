# Technical Skills - Interview Guide

This document outlines the technical skills demonstrated in the TravelMind AI project. Use this as a reference for interviews and portfolio discussions.

---

## Programming Language

### Python
- **Version:** 3.10+
- **Skills Demonstrated:**
  - Type hints and type annotations
  - Object-oriented programming (classes, inheritance)
  - Functional programming (decorators, generators)
  - Exception handling
  - Module organization and packaging
  - Standard library (sqlite3, threading, json, logging, pathlib)

---

## Frameworks

### LangGraph
- **Version:** 0.2.60
- **Skills Demonstrated:**
  - StateGraph construction
  - Node and edge definition
  - State management with reducers
  - Command-based routing
  - Parallel execution with `Command(goto=[...])`
  - Graph compilation and invocation

### LangChain
- **Version:** 0.3.14
- **Skills Demonstrated:**
  - PromptTemplate construction
  - Chain composition (`prompt | model | parser`)
  - JsonOutputParser for structured output
  - Runnable interface
  - Integration with Groq LLM

### Streamlit
- **Version:** 1.41.1
- **Skills Demonstrated:**
  - Multi-page application structure
  - Forms and user input handling
  - Session state management
  - Progress indicators and spinners
  - Expander-based layout
  - Error handling in UI

---

## AI Models

### Llama 3.1 (via Groq)
- **Model:** `groq/compound-mini`
- **Skills Demonstrated:**
  - LLM prompt engineering
  - Structured output generation
  - Temperature control for consistency
  - Multi-agent LLM orchestration

---

## External APIs

### OpenStreetMap (Nominatim)
- **Purpose:** Geocoding
- **Skills Demonstrated:**
  - REST API integration
  - HTTP request handling with `requests`
  - Response parsing
  - Rate limit awareness

### Open-Meteo
- **Purpose:** Weather data
- **Skills Demonstrated:**
  - Free API integration
  - Query parameter construction
  - JSON response parsing

### Tavily
- **Purpose:** Web search
- **Skills Demonstrated:**
  - SDK integration
  - Search query construction
  - Result extraction and processing

---

## Concepts

### Multi-Agent Systems
- **Skills Demonstrated:**
  - Agent specialization (9 agents with distinct roles)
  - Agent communication through shared state
  - Dependency-based orchestration
  - Supervisor pattern

### Agent Orchestration
- **Skills Demonstrated:**
  - Dynamic routing based on state
  - Dependency graph management
  - Supervisor pattern implementation
  - Extensible agent registration

### Parallel Execution
- **Skills Demonstrated:**
  - Concurrent agent execution
  - State merge with reducers
  - Race condition avoidance
  - Performance optimization

### Memory Management
- **Skills Demonstrated:**
  - SQLite database design
  - Schema creation and migration
  - Thread-safe connections
  - Data persistence patterns
  - Preference merging with COALESCE

### Structured Outputs
- **Skills Demonstrated:**
  - Pydantic model validation
  - JSON output parsing
  - Type-safe data contracts
  - Schema enforcement

### State Management
- **Skills Demonstrated:**
  - TypedDict state definition
  - Reducer functions for state updates
  - Partial state updates
  - State immutability

### Error Handling
- **Skills Demonstrated:**
  - Retry decorator pattern
  - Safe execution wrapper
  - Error accumulation in state
  - Graceful degradation
  - User-friendly error messages

---

## Summary

| Category | Technologies |
|----------|-------------|
| **Language** | Python 3.10+ |
| **Orchestration** | LangGraph |
| **LLM Framework** | LangChain |
| **Frontend** | Streamlit |
| **Backend** | FastAPI |
| **AI Models** | Llama 3.1 (Groq) |
| **APIs** | OpenStreetMap, Open-Meteo, Tavily |
| **Database** | SQLite |
| **Validation** | Pydantic |
| **Testing** | pytest |
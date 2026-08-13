import sys

# Ensure UTF-8 output on Windows consoles (handles ₹ and other Unicode).
_reconfigure = getattr(sys.stdout, "reconfigure", None)
if _reconfigure is not None:
    _reconfigure(encoding="utf-8")

from graph.travel_graph import run_travel_graph

result = run_travel_graph("Manali")

print("\n--- LOCATION ---")
print(result.get("location"))

print("\n--- WEATHER ---")
print(result.get("weather"))

print("\n--- SEARCH RESULTS ---")
print(result.get("search_results"))

print("\n--- BUDGET ---")
print(result.get("budget"))

print("\n--- ITINERARY ---")
print(result.get("itinerary"))

print("\n--- COMPLETED AGENTS ---")
print(result.get("completed_agents"))

print("\n--- ERRORS ---")
print(result.get("errors"))
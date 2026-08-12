from graph.travel_graph import create_graph


travel_graph = create_graph()

result = travel_graph.invoke({
    "destination": "Manali",
    "days": 3,
    "travelers": 2,
    "budget_per_day": 3000,
    "interests": ["nature", "adventure"],
    "travel_style": "budget",
})

print("\n--- LOCATION ---")
print(result["location"])

print("\n--- WEATHER ---")
print(result["weather"])

print("\n--- SEARCH RESULTS ---")
print(result["search_results"])

print("\n--- BUDGET ---")
print(result["budget"])
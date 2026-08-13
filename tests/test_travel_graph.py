# from graph.travel_graph import create_graph


# travel_graph = create_graph()

# result = travel_graph.invoke({
#     "destination": "Manali",
#     "days": 3,
#     "travelers": 2,
#     "budget_per_day": 3000,
#     "interests": ["nature", "adventure"],
#     "travel_style": "budget",
# })

# print("\n--- LOCATION ---")
# print(result.get("location"))

# print("\n--- WEATHER ---")
# print(result.get("weather"))

# print("\n--- SEARCH RESULTS ---")
# print(result.get("search_results"))

# print("\n--- BUDGET ---")
# print(result.get("budget"))

# print("\n--- ATTRACTIONS ---")
# print(result.get("places"))


from graph.travel_graph import run_travel_graph

result = run_travel_graph("Manali")

print("\n--- LOCATION ---")
print(result["location"])

print("\n--- WEATHER ---")
print(result["weather"])

print("\n--- SEARCH RESULTS ---")
print(result["search_results"])

print("\n--- BUDGET ---")
print(result["budget"])

print("\n--- ITINERARY ---")
print(result["itinerary"])
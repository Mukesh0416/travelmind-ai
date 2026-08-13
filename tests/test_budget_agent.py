from agents.budget_agent import budget_agent


state = {
    "destination": "Manali",
    "days": 3,
    "travelers": 2,
    "budget_per_day": 3000,
    "travel_style": "balanced",
}

result = budget_agent(state)

print("\n--- BUDGET ---")
print(result)
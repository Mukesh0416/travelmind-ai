from agents.budget_agent import budget_agent


result = budget_agent(
    daily_budget=3000,
    days=3,
    travelers=2,
)

print("\n--- BUDGET ---")
print(result)
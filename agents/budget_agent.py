from tools.budget_tool import calculate_budget


def budget_agent(
    daily_budget: float,
    days: int,
    travelers: int = 1,
):
    return calculate_budget(
        daily_budget=daily_budget,
        days=days,
        travelers=travelers,
    )
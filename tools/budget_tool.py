def calculate_budget(
    daily_budget: float,
    days: int,
    travelers: int = 1,
):
    total = daily_budget * days * travelers

    return {
        "daily_budget": daily_budget,
        "days": days,
        "travelers": travelers,
        "total_budget": total,
    }
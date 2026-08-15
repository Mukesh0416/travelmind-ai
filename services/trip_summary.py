"""
Trip summary generator for TravelMind AI.
Generates human-readable summaries of trip planning results.
"""

from datetime import datetime


def generate_trip_summary(result):
    """
    Generate a human-readable trip summary from the planning result.
    
    Args:
        result: The final state dict from plan_trip()
    
    Returns:
        str: Human-readable trip summary
    """
    itinerary = result.get("itinerary", {})
    budget = result.get("budget", {})
    hotels = result.get("hotels", [])
    restaurants = result.get("restaurants", [])
    transportation = result.get("transportation", {})
    packing_list = result.get("packing_list", [])
    
    destination = result.get("destination", "Unknown")
    days = itinerary.get("days", 0)
    travelers = result.get("travelers", 1)
    
    # Calculate total budget
    total_budget = budget.get("total_budget", 0) if budget else 0
    
    # Build summary
    lines = []
    lines.append("=" * 60)
    lines.append(f"Trip Overview: {destination}")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"Duration: {days} days")
    lines.append(f"Travelers: {travelers}")
    lines.append(f"Estimated Total Budget: ₹{total_budget:,.0f}")
    lines.append("")
    
    # Top attractions
    attractions = itinerary.get("day_plans", [])
    all_attractions = []
    for plan in attractions:
        all_attractions.append(plan.get("morning_attraction", ""))
        all_attractions.append(plan.get("afternoon_attraction", ""))
        all_attractions.append(plan.get("evening_activity", ""))
    
    lines.append("Top Attractions:")
    for i, attr in enumerate(set(a for a in all_attractions if a), 1):
        lines.append(f"  {i}. {attr}")
    lines.append("")
    
    # Recommended hotel
    if hotels:
        lines.append("Recommended Hotel:")
        for hotel in hotels[:3]:  # Top 3
            name = hotel.get("name", "N/A")
            price_range = hotel.get("price_range", "N/A")
            lines.append(f"  - {name} ({price_range})")
    else:
        lines.append("Recommended Hotel: N/A")
    lines.append("")
    
    # Recommended restaurant
    if restaurants:
        lines.append("Recommended Restaurants:")
        for restaurant in restaurants[:3]:  # Top 3
            name = restaurant.get("name", "N/A")
            cuisine = restaurant.get("cuisine", "N/A")
            lines.append(f"  - {name} ({cuisine})")
    else:
        lines.append("Recommended Restaurants: N/A")
    lines.append("")
    
    # Transportation plan
    if transportation:
        lines.append("Transportation Plan:")
        best_way = transportation.get("best_way_to_reach", "N/A")
        local_transport = transportation.get("local_transportation", "N/A")
        estimated_cost = transportation.get("estimated_cost", "N/A")
        lines.append(f"  Best way to reach: {best_way}")
        lines.append(f"  Local transportation: {local_transport}")
        lines.append(f"  Estimated cost: {estimated_cost}")
    else:
        lines.append("Transportation Plan: N/A")
    lines.append("")
    
    # Packing checklist
    if packing_list:
        lines.append("Packing Checklist:")
        for item in packing_list:
            category = item.get("category", "Miscellaneous")
            items = item.get("items", [])
            lines.append(f"  {category}:")
            for sub_item in items[:5]:  # Show first 5 items per category
                lines.append(f"    - {sub_item}")
            if len(items) > 5:
                lines.append(f"    ... and {len(items) - 5} more")
    else:
        lines.append("Packing Checklist: N/A")
    lines.append("")
    
    # Itinerary overview
    lines.append("Itinerary Summary:")
    for plan in itinerary.get("day_plans", []):
        day = plan.get("day", "N/A")
        morning = plan.get("morning_activity", "N/A")
        lines.append(f"  Day {day}: {morning}")
    lines.append("")
    
    lines.append("=" * 60)
    
    return "\n".join(lines)


def generate_quick_summary(result):
    """
    Generate a quick one-line trip summary.
    
    Args:
        result: The final state dict from plan_trip()
    
    Returns:
        str: Quick trip summary
    """
    destination = result.get("destination", "Unknown")
    days = result.get("itinerary", {}).get("days", 0)
    budget = result.get("budget", {})
    total_budget = budget.get("total_budget", 0) if budget else 0
    hotels = result.get("hotels", [])
    restaurant_names = [r.get("name", "N/A") for r in result.get("restaurants", [])[:1]]
    
    hotel_info = hotels[0].get("name", "N/A") if hotels else "N/A"
    restaurant_info = restaurant_names[0] if restaurant_names else "N/A"
    
    return f"{destination} - {days} days trip, ₹{total_budget:,.0f} budget, Stay at {hotel_info}, Dine at {restaurant_info}"
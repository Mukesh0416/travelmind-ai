"""
Service layer for TravelMind AI trip planning.
Provides a unified entry point for planning trips with consistent output structure.
"""

from graph.travel_graph import run_travel_graph
from services.memory import memory
from services.agent_utils import logger
from datetime import datetime
import json


def plan_trip(
    destination,
    days,
    travelers,
    budget_per_day,
    interests=None,
    travel_style="balanced",
    user_id=None
):
    """
    Plan a trip using the multi-agent system.
    
    This is the single entry point for trip planning that:
    - Loads user preferences and travel history
    - Builds the initial state
    - Invokes the LangGraph multi-agent system
    - Saves updated memory
    - Returns the final structured state
    
    Args:
        destination: Trip destination
        days: Number of days for the trip
        travelers: Number of travelers
        budget_per_day: Budget per day in local currency
        interests: List of user interests (optional)
        travel_style: Travel style preference (e.g., 'balanced', 'luxury', 'budget')
        user_id: User identifier for memory persistence (optional)
    
    Returns:
        dict: Final state containing trip results with standardized structure
    """
    logger.info(f"[Service] Starting trip planning for {destination}")
    
    # Build initial state
    state = {
        "destination": destination,
        "days": days,
        "travelers": travelers,
        "budget_per_day": budget_per_day,
        "interests": interests or [],
        "travel_style": travel_style,
    }
    
    # Load user preferences from memory if user_id provided
    if user_id:
        try:
            preferences = memory.get_preferences(user_id)
            state["preferences"] = preferences
            logger.info(f"[Service] Loaded preferences for user {user_id}")
        except Exception as e:
            logger.warning(f"[Service] Could not load preferences for user {user_id}: {e}")
            state["preferences"] = {}
    
    # Ensure completed_agents tracker is present
    state.setdefault("completed_agents", {
        "location": False,
        "weather": False,
        "search": False,
        "budget": False,
        "accommodation": False,
        "restaurant": False,
        "transportation": False,
        "packing": False,
        "itinerary": False,
    })
    
    # Invoke the travel planning graph
    logger.info(f"[Service] Invoking travel planning graph for {destination}")
    start_time = datetime.now()
    
    try:
        result = run_travel_graph(state=state)
        execution_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"[Service] Graph completed in {execution_time:.2f}s")
    except Exception as e:
        logger.error(f"[Service] Graph execution failed: {e}")
        raise
    
    # Save updated memory if user_id provided
    if user_id:
        try:
            # Extract destination from result for travel history
            destination_result = result.get("destination", destination)
            memory.add_previous_destination(user_id, destination_result)
            logger.info(f"[Service] Saved destination to travel history for user {user_id}")
        except Exception as e:
            logger.warning(f"[Service] Could not save travel history for user {user_id}: {e}")
    
    logger.info(f"[Service] Trip planning completed for {destination}")
    
    return result
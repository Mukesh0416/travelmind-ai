"""
Simple in-memory user preference store.

This provides a lightweight memory layer for personalizing travel plans.
Future enhancements can replace this with Redis, LangGraph memory,
or persistent session storage without changing agent code.
"""

from typing import Dict, Optional


class UserMemory:
    """
    Stores user preferences keyed by user_id.

    Each user has a dict of preferences such as:

    - preferred_cuisine
    - preferred_hotel_category
    - adventure_level
    - previous_destinations
    - budget_preferences
    - favorite_activities
    """

    def __init__(self):
        self._store: Dict[str, dict] = {}

    def get_preferences(self, user_id: str) -> dict:
        """Return the preferences dict for a user (empty if none)."""

        return self._store.get(user_id, {})

    def set_preferences(self, user_id: str, preferences: dict) -> dict:
        """Merge new preferences into the user's stored preferences."""

        current = self._store.get(user_id, {})
        current.update(preferences)
        self._store[user_id] = current

        return current

    def add_previous_destination(self, user_id: str, destination: str) -> dict:
        """Append a destination to the user's travel history."""

        current = self._store.get(user_id, {})

        previous = current.get("previous_destinations", [])

        if destination not in previous:
            previous.append(destination)

        current["previous_destinations"] = previous

        self._store[user_id] = current

        return current

    def clear(self, user_id: str) -> None:
        """Remove all stored preferences for a user."""

        self._store.pop(user_id, None)


# Global in-memory memory instance.
memory = UserMemory()
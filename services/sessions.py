"""
Session management for TravelMind AI.
Handles user sessions, preferences, and travel history.
"""

import json
import os
from datetime import datetime
from memory.memory import memory


class SessionManager:
    """
    Manages user sessions with persistent storage.
    
    Stores:
    - User ID
    - Preferences
    - Travel history
    - Previous trips
    """
    
    def __init__(self, user_id=None):
        self.user_id = user_id
        self._preferences = None
        self._travel_history = None
        self._created_at = datetime.now().isoformat()
    
    @property
    def preferences(self):
        """Get user preferences."""
        if self._preferences is None and self.user_id:
            self._preferences = memory.get_preferences(self.user_id)
        return self._preferences or {}
    
    @preferences.setter
    def preferences(self, prefs):
        """Set user preferences."""
        if self.user_id:
            memory.set_preferences(self.user_id, prefs)
            self._preferences = prefs
    
    @property
    def travel_history(self):
        """Get user travel history."""
        if self._travel_history is None and self.user_id:
            self._travel_history = memory.get_trip_history(self.user_id)
        return self._travel_history or []
    
    def save_trip(self, destination, days=None, budget=None):
        """Save a completed trip to user's travel history."""
        if self.user_id:
            memory.save_trip(self.user_id, destination, days, budget)
            # Refresh cached history
            self._travel_history = memory.get_trip_history(self.user_id)
    
    def add_previous_destination(self, destination):
        """Add a destination to user's previous destinations list."""
        if self.user_id:
            memory.add_previous_destination(self.user_id, destination)
            # Refresh cached preferences
            self._preferences = memory.get_preferences(self.user_id)
    
    def to_dict(self):
        """Convert session to dictionary for serialization."""
        return {
            "user_id": self.user_id,
            "created_at": self._created_at,
            "preferences": self._preferences or {},
            "travel_history": self._travel_history or [],
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create session from dictionary."""
        session = cls(user_id=data.get("user_id"))
        session._created_at = data.get("created_at", datetime.now().isoformat())
        session._preferences = data.get("preferences", {})
        session._travel_history = data.get("travel_history", [])
        return session


def create_session(user_id):
    """Create a new user session."""
    memory.create_user(user_id)
    return SessionManager(user_id)


def get_session(user_id):
    """Get or create a session for a user."""
    return SessionManager(user_id)
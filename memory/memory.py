"""
Persistent SQLite-backed user memory store.

Sprint 1: Persistent Memory
---------------------------
Creates a structured SQLite database with three tables:

users
    user_id     TEXT PRIMARY KEY
    name        TEXT
    created_at  TEXT

preferences
    user_id               TEXT PRIMARY KEY
    travel_style          TEXT
    budget_range          TEXT
    preferred_hotel_type  TEXT
    preferred_food        TEXT
    favorite_activities   TEXT    (JSON-encoded list)
    updated_at            TEXT

travel_history
    user_id      TEXT
    destination  TEXT
    days         INTEGER
    budget       REAL
    created_at   TEXT

The database file and all tables are created automatically on first use.
Timestamps are stored as ISO-8601 UTC strings. The schema supports any
number of users.

The legacy `user_memory` JSON-blob table is retained ONLY for backward
compatibility with the existing graph/backend/agent callers, whose
dict-based `preferences` interface is preserved. The new structured
columns are populated in parallel so later sprints can migrate callers
onto the structured API.
"""

from __future__ import annotations

import json
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

# SQLite database file stored in the project root.
DB_PATH = Path(__file__).resolve().parent.parent / "travelmind_memory.db"

# One connection per thread keeps SQLite safe inside FastAPI / LangGraph.
_thread_local = threading.local()

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------
#
# All four tables are created with IF NOT EXISTS so both fresh databases and
# databases created by the previous Phase 1 schema are handled correctly.

SCHEMA = """
CREATE TABLE IF NOT EXISTS user_memory (
    user_id     TEXT PRIMARY KEY,
    preferences TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    user_id    TEXT PRIMARY KEY,
    name       TEXT DEFAULT '',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS preferences (
    user_id              TEXT PRIMARY KEY,
    travel_style         TEXT,
    budget_range         TEXT,
    preferred_hotel_type TEXT,
    preferred_food       TEXT,
    favorite_activities  TEXT,
    updated_at           TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS travel_history (
    user_id     TEXT NOT NULL,
    destination TEXT NOT NULL,
    days        INTEGER,
    budget      REAL,
    created_at  TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_preferences_user
    ON preferences (user_id);

CREATE INDEX IF NOT EXISTS idx_travel_history_user
    ON travel_history (user_id);
"""


def _now() -> str:
    """Return the current UTC time as an ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()


def _get_connection() -> sqlite3.Connection:
    """Return a thread-local SQLite connection, creating the schema if needed."""

    conn = getattr(_thread_local, "connection", None)

    if conn is None:

        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        conn.executescript(SCHEMA)
        conn.commit()

        _thread_local.connection = conn

    return conn


# ---------------------------------------------------------------------------
# Structured <-> dict helpers
# ---------------------------------------------------------------------------

PREFERENCE_FIELDS = (
    "travel_style",
    "budget_range",
    "preferred_hotel_type",
    "preferred_food",
    "favorite_activities",
)


def _row_to_preferences(row: Optional[sqlite3.Row]) -> dict:
    """Convert a `preferences` table row into a plain dict."""

    if row is None:
        return {}

    result = {}

    for field in PREFERENCE_FIELDS:

        value = row[field]

        if value is None:
            continue

        if field == "favorite_activities":

            try:
                result[field] = json.loads(value)
            except (json.JSONDecodeError, TypeError):
                result[field] = []

        else:
            result[field] = value

    return result


def _extract_structured(preferences: dict) -> dict:
    """
    Pull the structured preference fields out of an arbitrary preference dict.

    Also handles nested `hotel_preferences` / `restaurant_preferences`
    dicts that the legacy agents may have stored.
    """

    if not preferences:
        return {}

    hotel_prefs = preferences.get("hotel_preferences") or {}
    restaurant_prefs = preferences.get("restaurant_preferences") or {}

    structured = {}

    travel_style = preferences.get("travel_style")
    if travel_style is not None:
        structured["travel_style"] = travel_style

    budget_range = preferences.get("budget_range")
    if budget_range is not None:
        structured["budget_range"] = budget_range

    preferred_hotel_type = (
        preferences.get("preferred_hotel_type")
        or hotel_prefs.get("preferred_hotel_type")
    )
    if preferred_hotel_type is not None:
        structured["preferred_hotel_type"] = preferred_hotel_type

    preferred_food = (
        preferences.get("preferred_food")
        or restaurant_prefs.get("preferred_food")
    )
    if preferred_food is not None:
        structured["preferred_food"] = preferred_food

    favorite_activities = preferences.get("favorite_activities")
    if favorite_activities is not None:
        structured["favorite_activities"] = favorite_activities

    return structured


class UserMemory:
    """
    Persistent user memory backed by SQLite.

    Legacy interface (kept so existing graph/backend/agent code does not
    need to change):

    - get_preferences(user_id)
    - set_preferences(user_id, preferences)
    - add_previous_destination(user_id, destination)
    - clear(user_id)
    - all_users()

    New structured methods:

    - create_user(user_id, name="")
    - save_trip(user_id, destination, days=None, budget=None)
    - get_trip_history(user_id)
    """

    # -- users ---------------------------------------------------------------

    def create_user(self, user_id: str, name: str = "") -> dict:
        """
        Create a user row if it does not already exist.

        Returns a dict describing the created user.
        """

        if not user_id:
            raise ValueError("user_id is required")

        now = _now()

        conn = _get_connection()

        conn.execute(
            """
            INSERT OR IGNORE INTO users (user_id, name, created_at)
            VALUES (?, ?, ?)
            """,
            (user_id, name, now),
        )
        conn.commit()

        return {
            "user_id": user_id,
            "name": name,
            "created_at": now,
        }

    # -- preferences ------------------------------------------------------------

    def get_preferences(self, user_id: str) -> dict:
        """
        Return the preference dict for a user (empty if none).

        Merges the legacy JSON blob with the structured `preferences`
        table so data written through either path is returned.
        """

        conn = _get_connection()

        # Legacy blob (kept for backward compatibility).
        row = conn.execute(
            "SELECT preferences FROM user_memory WHERE user_id = ?",
            (user_id,),
        ).fetchone()

        preferences = {}

        if row is not None:

            try:
                preferences = json.loads(row["preferences"])
            except (json.JSONDecodeError, TypeError):
                preferences = {}

        # Structured table values take precedence for the known fields.
        structured = conn.execute(
            "SELECT * FROM preferences WHERE user_id = ?",
            (user_id,),
        ).fetchone()

        if structured is not None:
            preferences.update(_row_to_preferences(structured))

        return preferences

    def set_preferences(self, user_id: str, preferences: dict) -> dict:
        """
        Merge new preferences into the user's stored preferences.

        Writes both the legacy JSON blob (for compatibility) and the new
        structured `preferences` columns (for Sprint 2+).
        """

        merged = dict(self.get_preferences(user_id))
        merged.update(preferences or {})

        conn = _get_connection()

        # Legacy blob (kept for backward compatibility).
        conn.execute(
            """
            INSERT INTO user_memory (user_id, preferences)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                preferences = excluded.preferences
            """,
            (user_id, json.dumps(merged)),
        )

        # Structured table. COALESCE preserves existing values when a field
        # is absent from a partial update.
        structured = _extract_structured(merged)
        now = _now()

        favorite_activities = structured.get("favorite_activities")

        conn.execute(
            """
            INSERT INTO preferences (
                user_id, travel_style, budget_range,
                preferred_hotel_type, preferred_food,
                favorite_activities, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                travel_style         = COALESCE(
                    excluded.travel_style, preferences.travel_style
                ),
                budget_range         = COALESCE(
                    excluded.budget_range, preferences.budget_range
                ),
                preferred_hotel_type = COALESCE(
                    excluded.preferred_hotel_type,
                    preferences.preferred_hotel_type
                ),
                preferred_food       = COALESCE(
                    excluded.preferred_food, preferences.preferred_food
                ),
                favorite_activities  = COALESCE(
                    excluded.favorite_activities,
                    preferences.favorite_activities
                ),
                updated_at           = excluded.updated_at
            """,
            (
                user_id,
                structured.get("travel_style"),
                structured.get("budget_range"),
                structured.get("preferred_hotel_type"),
                structured.get("preferred_food"),
                json.dumps(favorite_activities)
                if favorite_activities is not None else None,
                now,
            ),
        )

        # Ensure a users row exists for the user.
        conn.execute(
            """
            INSERT OR IGNORE INTO users (user_id, name, created_at)
            VALUES (?, '', ?)
            """,
            (user_id, now),
        )

        conn.commit()

        return merged

    # -- travel history ---------------------------------------------------------

    def add_previous_destination(self, user_id: str, destination: str) -> dict:
        """
        Append a destination to the user's travel history.

        Updates the legacy blob AND records a row in the structured
        `travel_history` table.
        """

        current = self.get_preferences(user_id)

        previous = current.get("previous_destinations", [])

        if not isinstance(previous, list):
            previous = []

        if destination and destination not in previous:
            previous.append(destination)

        current["previous_destinations"] = previous

        result = self.set_preferences(user_id, current)

        # Also record in the structured travel_history table.
        if destination:
            self.save_trip(user_id, destination)

        return result

    def save_trip(
        self,
        user_id: str,
        destination: str,
        days: Optional[int] = None,
        budget: Optional[float] = None,
    ) -> dict:
        """
        Record a completed trip in the structured `travel_history` table.

        Returns a dict describing the saved trip.
        """

        now = _now()

        conn = _get_connection()

        conn.execute(
            """
            INSERT INTO travel_history
                (user_id, destination, days, budget, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, destination, days, budget, now),
        )
        conn.commit()

        return {
            "user_id": user_id,
            "destination": destination,
            "days": days,
            "budget": budget,
            "created_at": now,
        }

    def get_trip_history(self, user_id: str) -> List[dict]:
        """
        Return the structured trip history for a user, newest first.
        """

        conn = _get_connection()

        rows = conn.execute(
            """
            SELECT destination, days, budget, created_at
            FROM travel_history
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,),
        ).fetchall()

        return [
            {
                "destination": row["destination"],
                "days": row["days"],
                "budget": row["budget"],
                "created_at": row["created_at"],
            }
            for row in rows
        ]

    # -- maintenance --------------------------------------------------------

    def clear(self, user_id: str) -> None:
        """Remove all stored data for a user from every table."""

        conn = _get_connection()

        conn.execute("DELETE FROM user_memory WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM preferences WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM travel_history WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()

    def all_users(self) -> Dict[str, dict]:
        """Return all stored user preferences (for diagnostics/testing)."""

        conn = _get_connection()

        rows = conn.execute(
            "SELECT user_id, preferences FROM user_memory"
        ).fetchall()

        result: Dict[str, dict] = {}

        for row in rows:

            try:
                result[row["user_id"]] = json.loads(row["preferences"])
            except (json.JSONDecodeError, TypeError):
                continue

        # Merge in the structured preference values as well.
        for user_id in list(result.keys()):
            result[user_id] = self.get_preferences(user_id)

        return result


# Global memory instance (interface-compatible with the old in-memory store).
memory = UserMemory()
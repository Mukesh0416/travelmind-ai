"""
Sprint 1 verification: Persistent Memory.

Checks that the SQLite database is created automatically with the
required tables, timestamps are stored, multiple users are supported,
and the legacy interface still works.
"""

import json
import sqlite3
import sys
import tempfile
from pathlib import Path

# Ensure UTF-8 output on Windows consoles.
_reconfigure = getattr(sys.stdout, "reconfigure", None)
if _reconfigure is not None:
    _reconfigure(encoding="utf-8")

# Add the project root to sys.path so `services` is importable
# when this file is run directly (python tests/test_memory_sprint1.py).
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

# Point the memory store at a temporary database so we do not touch
# the real travelmind_memory.db during tests.
import importlib
memory_module = importlib.import_module("memory.memory")

_TMP_DIR = tempfile.mkdtemp(prefix="travelmind_sprint1_")
memory_module.DB_PATH = Path(_TMP_DIR) / "test_memory.db"

# Reset the thread-local connection so the new DB path is used.
memory_module._thread_local.connection = None

from memory.memory import memory  # noqa: E402

REQUIRED_TABLES = {"users", "preferences", "travel_history"}

failures = []


def check(condition, message):
    if condition:
        print(f"  ✓ {message}")
    else:
        print(f"  ✗ {message}")
        failures.append(message)


print("=== Sprint 1: Persistent Memory ===")

# --- 1. Database and tables created automatically -------------------------
print("\n[1] Database and tables created automatically")

# Trigger schema creation (the DB and tables are created lazily on first use).
memory.get_preferences("__schema_check__")

conn = sqlite3.connect(str(memory_module.DB_PATH))
tables = {
    row[0]
    for row in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()
}
conn.close()

check(
    REQUIRED_TABLES.issubset(tables),
    f"All required tables exist: {sorted(REQUIRED_TABLES)}",
)
check(
    "user_memory" in tables,
    "Legacy user_memory table retained for backward compatibility",
)

# --- 2. Timestamps stored -------------------------------------------------
print("\n[2] Timestamps stored")

memory.create_user("user_a", name="Alice")

conn = sqlite3.connect(str(memory_module.DB_PATH))
row = conn.execute(
    "SELECT created_at FROM users WHERE user_id = 'user_a'"
).fetchone()
conn.close()

check(row is not None, "users.created_at is populated")
check(row is not None and row[0], "users.created_at is a non-empty string")

# --- 3. Multiple users supported ------------------------------------------
print("\n[3] Multiple users supported")

memory.create_user("user_b", name="Bob")

memory.set_preferences(
    "user_a",
    {
        "travel_style": "adventure",
        "budget_range": "mid-range",
        "preferred_hotel_type": "mountain resort",
        "preferred_food": "local cuisine",
        "favorite_activities": ["trekking", "camping"],
    },
)

memory.set_preferences(
    "user_b",
    {
        "travel_style": "luxury",
        "budget_range": "luxury",
        "preferred_hotel_type": "5-star",
        "preferred_food": "fine dining",
        "favorite_activities": ["spa", "golf"],
    },
)

prefs_a = memory.get_preferences("user_a")
prefs_b = memory.get_preferences("user_b")

check(prefs_a.get("travel_style") == "adventure", "user_a travel_style = adventure")
check(prefs_b.get("travel_style") == "luxury", "user_b travel_style = luxury")
check(prefs_a.get("budget_range") == "mid-range", "user_a budget_range = mid-range")
check(prefs_b.get("budget_range") == "luxury", "user_b budget_range = luxury")
check(
    prefs_a.get("preferred_hotel_type") == "mountain resort",
    "user_a preferred_hotel_type = mountain resort",
)
check(
    prefs_b.get("preferred_hotel_type") == "5-star",
    "user_b preferred_hotel_type = 5-star",
)
check(
    prefs_a.get("favorite_activities") == ["trekking", "camping"],
    "user_a favorite_activities stored as list",
)

# --- 4. Structured preferences table populated ----------------------------
print("\n[4] Structured preferences table populated")

conn = sqlite3.connect(str(memory_module.DB_PATH))
row = conn.execute(
    """
    SELECT travel_style, budget_range, preferred_hotel_type,
           preferred_food, favorite_activities, updated_at
    FROM preferences
    WHERE user_id = 'user_a'
    """
).fetchone()
conn.close()

check(row is not None, "preferences row exists for user_a")
check(row is not None and row[0] == "adventure", "preferences.travel_style = adventure")
check(row is not None and row[1] == "mid-range", "preferences.budget_range = mid-range")
check(
    row is not None and row[2] == "mountain resort",
    "preferences.preferred_hotel_type = mountain resort",
)
check(
    row is not None and row[3] == "local cuisine",
    "preferences.preferred_food = local cuisine",
)
check(
    row is not None and json.loads(row[4]) == ["trekking", "camping"],
    "preferences.favorite_activities stored as JSON list",
)
check(
    row is not None and row[5],
    "preferences.updated_at is populated",
)

# --- 5. Travel history table ----------------------------------------------
print("\n[5] Travel history table")

memory.save_trip("user_a", "Manali", days=3, budget=18000)
memory.save_trip("user_a", "Kasol", days=2, budget=12000)

history = memory.get_trip_history("user_a")

check(len(history) == 2, f"2 trips recorded for user_a (got {len(history)})")
check(
    history[0]["destination"] == "Kasol",
    "Newest trip first (Kasol)",
)
check(
    history[1]["destination"] == "Manali",
    "Older trip second (Manali)",
)
check(
    history[1]["days"] == 3 and history[1]["budget"] == 18000,
    "Trip stores days and budget",
)
check(
    all("created_at" in trip for trip in history),
    "Each trip has a created_at timestamp",
)

# --- 6. Legacy interface still works --------------------------------------
print("\n[6] Legacy interface backward compatibility")

memory.add_previous_destination("user_a", "Goa")

prefs_after = memory.get_preferences("user_a")

check(
    "Goa" in prefs_after.get("previous_destinations", []),
    "add_previous_destination still updates previous_destinations",
)

# --- 7. Cleanup -----------------------------------------------------------
print("\n[7] Cleanup")

memory.clear("user_a")
memory.clear("user_b")

check(memory.get_preferences("user_a") == {}, "user_a cleared")
check(memory.get_preferences("user_b") == {}, "user_b cleared")
check(memory.get_trip_history("user_a") == [], "user_a trip history cleared")

print()
if failures:
    print(f"FAILED: {len(failures)} check(s) failed")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
else:
    print("ALL SPRINT 1 CHECKS PASSED")
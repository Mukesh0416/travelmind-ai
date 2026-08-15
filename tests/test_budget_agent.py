import sys
from pathlib import Path

# Add the project root to sys.path so imports work when run directly.
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

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